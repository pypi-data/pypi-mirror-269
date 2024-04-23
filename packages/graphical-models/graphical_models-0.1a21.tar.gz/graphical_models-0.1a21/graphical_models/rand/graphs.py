# === IMPORTS: BUILT-IN ===
import random
import itertools as itr
from functools import partial
from typing import Union, List, Callable, Optional, Any, Dict

# === IMPORTS: THIRD-PARTY ===
import numpy as np
from tqdm import tqdm
from scipy.special import comb
from networkx import barabasi_albert_graph, fast_gnp_random_graph

# === IMPORTS: LOCAL ===
from graphical_models import DAG, GaussDAG, SampleDAG, CamDAG
from graphical_models.classes.dags.discrete_dag import DiscreteDAG

# class RandWeightFn(Protocol):
#     def __call__(self, size: int) -> Union[float, List[float]]: ...


RandWeightFn = Any


def _coin(p, size=1):
    return np.random.binomial(1, p, size=size)


def unif_away_zero(low=.25, high=1, size=1, all_positive=False):
    if all_positive:
        return np.random.uniform(low, high, size=size)
    signs = (_coin(.5, size) - .5) * 2
    return signs * np.random.uniform(low, high, size=size)


def unif_away_original(original, dist_original=.25, low=.25, high=1):
    if dist_original < low:
        raise ValueError(
            "the lowest absolute value of weights must be larger than the distance between old weights and new weights")
    regions = []
    if original < 0:
        regions.append((low, high))
        if original - dist_original >= -high:
            regions.append((-high, original - dist_original))
        if original + dist_original <= -low:
            regions.append((original + dist_original, -low))
    else:
        regions.append((-high, -low))
        if original + dist_original <= high:
            regions.append((original + dist_original, high))
        if original - dist_original >= low:
            regions.append((low, original - dist_original))
    a, b = random.choices(regions, weights=[b - a for a, b in regions])[0]
    return np.random.uniform(a, b)


def directed_erdos(
        nnodes,
        density=None,
        exp_nbrs=None,
        size=1,
        as_list=False,
        random_order=True
) -> Union[DAG, List[DAG]]:
    """
    Generate random Erdos-Renyi DAG(s) on `nnodes` nodes with density `density`.

    Parameters
    ----------
    nnodes:
        Number of nodes in each graph.
    density:
        Probability of any edge.
    size:
        Number of graphs.
    as_list:
        If True, always return as a list, even if only one DAG is generated.

    Examples
    --------
    >>> from graphical_models.rand import directed_erdos
    >>> d = directed_erdos(5, .5)
    """
    assert density is not None or exp_nbrs is not None
    density = density if density is not None else exp_nbrs / (nnodes - 1)
    if size == 1:
        # if density < .01:
        #     print('here')
        #     random_nx = fast_gnp_random_graph(nnodes, density, directed=True)
        #     d = DAG(nodes=set(range(nnodes)), arcs=random_nx.edges)
        #     return [d] if as_list else d
        bools = _coin(density, size=int(nnodes * (nnodes - 1) / 2))
        arcs = {(i, j) for (i, j), b in zip(itr.combinations(range(nnodes), 2), bools) if b}
        d = DAG(nodes=set(range(nnodes)), arcs=arcs)
        if random_order:
            nodes = list(range(nnodes))
            d = d.rename_nodes(dict(enumerate(np.random.permutation(nodes))))
        return [d] if as_list else d
    else:
        return [directed_erdos(nnodes, density, random_order=random_order) for _ in range(size)]


def directed_erdos_with_confounders(
        nnodes: int,
        density: Optional[float] = None,
        exp_nbrs: Optional[float] = None,
        num_confounders: int = 1,
        confounder_pervasiveness: float = 1,
        size=1,
        as_list=False,
        random_order=True
) -> Union[DAG, List[DAG]]:
    assert density is not None or exp_nbrs is not None
    density = density if density is not None else exp_nbrs / (nnodes - 1)

    if size == 1:
        confounders = list(range(num_confounders))
        nonconfounders = list(range(num_confounders, nnodes+num_confounders))
        bools = _coin(confounder_pervasiveness, size=int(num_confounders*nnodes))
        confounder_arcs = {(i, j) for (i, j), b in zip(itr.product(confounders, nonconfounders), bools) if b}
        bools = _coin(density, size=int(nnodes * (nnodes - 1) / 2))
        local_arcs = {(i, j) for (i, j), b in zip(itr.combinations(nonconfounders, 2), bools) if b}
        d = DAG(nodes=set(range(nnodes)), arcs=confounder_arcs|local_arcs)

        if random_order:
            nodes = list(range(nnodes+num_confounders))
            d = d.rename_nodes(dict(enumerate(np.random.permutation(nodes))))

        return [d] if as_list else d
    else:
        return [
            directed_erdos_with_confounders(
                nnodes,
                density,
                num_confounders=num_confounders,
                confounder_pervasiveness=confounder_pervasiveness,
                random_order=random_order
            )
            for _ in range(size)
        ]


def rand_weights(dag, rand_weight_fn: RandWeightFn = unif_away_zero) -> GaussDAG:
    """
    Generate a GaussDAG from a DAG, with random edge weights independently drawn from `rand_weight_fn`.

    Parameters
    ----------
    dag:
        DAG
    rand_weight_fn:
        Function to generate random weights.

    Examples
    --------
    >>> import causaldag as cd
    >>> d = cd.DAG(arcs={(1, 2), (2, 3)})
    >>> g = cd.rand.rand_weights(d)
    """
    weights = rand_weight_fn(size=len(dag.arcs))
    return GaussDAG(nodes=list(range(len(dag.nodes))), arcs=dict(zip(dag.arcs, weights)))


def rand_discrete_dag(dag, node_alphabets=None, alpha=1.0):
    if node_alphabets is None:
        node_alphabets = {node: list(range(3)) for node in dag.nodes}
    
    conditionals = dict()
    node2parents = dict()
    for node in dag.nodes:
        parents = list(dag.parents_of(node))
        node2parents[node] = parents
        K = len(node_alphabets[node])

        if len(parents) == 0:
            conditional = np.random.dirichlet([alpha] * K)
        if len(parents) != 0:
            parent_alphabet_shape = [len(node_alphabets[p]) for p in parents]
            conditional = np.random.dirichlet([alpha] * K, size=parent_alphabet_shape)
        conditionals[node] = conditional
    
    dag = DiscreteDAG(
        nodes=list(range(dag.nnodes)), 
        arcs=dag.arcs,
        conditionals=conditionals,
        node2parents=node2parents,
        node_alphabets=node_alphabets
    )

    return dag


def tensor_product(vecs):
    current_prod = vecs[0]
    for i in range(1, len(vecs)):
        new_vec = vecs[i]
        current_prod = np.tensordot(current_prod, new_vec, axes=0)
    return current_prod


def rand_noisy_or_dag(dag, q_low=0.75, q_high=1.0, p_low=0.5, p_high=1.0):
    conditionals = dict()
    node2parents = dict()
    for node in dag.nodes:
        parents = list(dag.parents_of(node))
        node2parents[node] = parents
        
        q_j = np.random.uniform(q_low, q_high)
        # q_j = 1
        if len(parents) > 0:
            parent_params = np.random.uniform(p_low, p_high, size=len(parents))
            vecs = np.vstack((np.ones(len(parents)), parent_params)).T
            prob0 = tensor_product(vecs)
            prob0 = prob0 * q_j
            conditional = np.stack((prob0, 1 - prob0), axis=-1)
        else:
            prob0 = np.random.uniform(0, 1) * q_j
            conditional = np.array([prob0, 1 - prob0])

        conditionals[node] = conditional
    
    dag = DiscreteDAG(
        nodes=list(range(dag.nnodes)), 
        arcs=dag.arcs,
        conditionals=conditionals,
        node2parents=node2parents,
        node_alphabets={i: [0, 1] for i in range(dag.nnodes)}
    )

    return dag


def rand_normal_wishart(dag, var_dof=None, edge_scale=1, edge_mean=0):
    arcs = dict()
    variances = []
    means = []
    var_dof = var_dof if var_dof is not None else dag.nnodes + 1
    nodes = list(dag.nodes)
    for node in nodes:
        parents = dag.parents_of(node)
        var_node = np.random.chisquare((var_dof - dag.nnodes + len(parents) + 1)/2)
        weights = np.random.normal(edge_mean, var_node * edge_scale, size=len(parents) + 1)
        variances.append(var_node)
        means.append(weights[-1])
        arcs.update({(parent, node): weight for parent, weight in zip(parents, weights[:-1])})
    return GaussDAG(nodes=list(dag.nodes), arcs=arcs, biases=means, variances=variances)


def _leaky_relu(vals):
    return np.where(vals > 0, vals, vals * .01)


def rand_nn_functions(
        dag: DAG,
        num_layers=3,
        nonlinearity=_leaky_relu,
        noise=lambda: np.random.laplace(0, 1)
) -> SampleDAG:
    s = SampleDAG(dag._nodes, arcs=dag._arcs)

    # for each node, create the conditional
    for node in dag._nodes:
        nparents = dag.indegree_of(node)
        layer_mats = [np.random.rand(nparents, nparents) * 2 for _ in range(num_layers)]

        def conditional(parent_vals):
            vals = parent_vals
            for a in layer_mats:
                vals = a @ vals
                vals = nonlinearity(vals)
            return vals + noise()

        s.set_conditional(node, conditional)

    return s


def _cam_conditional(parent_vals, c_node, parent_weights, parent_bases, noise):
    return sum([
        c_node * weight * base(val) for weight, base, val in zip(parent_weights, parent_bases, parent_vals)
    ]) + noise()


def _cam_mean_function(
        parent_vals: np.ndarray,
        parents: list,
        c_node: float,
        parent_weights: np.ndarray,
        parent2base: dict
):
    assert parent_vals.shape[1] == len(parents)
    assert len(parent_weights) == len(parents)
    assert all(parent in parent2base for parent in parents)

    if len(parents) == 0:
        return np.zeros(parent_vals.shape[0])
    parent_contribs = np.array([parent2base[parent](parent_vals[:, ix]) for ix, parent in enumerate(parents)]).T
    parent_contribs = parent_contribs * parent_weights
    parent_contrib = parent_contribs.sum(axis=1)
    return c_node * parent_contrib


def rand_additive_basis(
        dag: DAG,
        basis: list,
        r2_dict: Optional[Union[Dict[int, float], float]] = None,
        rand_weight_fn: RandWeightFn = unif_away_zero,
        noise=lambda size: np.random.normal(0, 1, size=size),
        num_monte_carlo: int = 10000,
        progress=False,
        r2_key="nparents"
):
    """
    Generate a random structural causal model (SCM), using `dag` as the structure, and with each variable
    being a general additive model (GAM) of its parents.

    Parameters
    ----------
    dag:
        A DAG to use as the structure for the model.
    basis:
        Basis functions for the GAM.
    r2_dict:
        A dictionary mapping each number of parents to the desired signal-to-noise ratio (SNR) for nodes
        with that many parents. By default, 1/2 for any number of parents.
    rand_weight_fn:
        A function to generate random weights for each parent.
    noise:
        A function to generate random internal noise for each node.
    internal_variance:
        The variance of the above noise function.
    num_monte_carlo:
        The number of Monte Carlo samples used when computing coefficients to achieve the desired SNR.

    Examples
    --------
    >>> import causaldag as cd
    >>> import numpy as np
    >>> d = cd.DAG(arcs={(1, 2), (2, 3), (1, 3)})
    >>> basis = [np.sin, np.cos, np.exp]
    >>> r2_dict = {1: 1/2, 2: 2/3}
    >>> g = cd.rand.rand_additive_basis(d, basis, r2_dict)
    """
    if r2_dict is None:
        r2_dict = {nparents: 1/2 for nparents in range(dag.nnodes)}
    if isinstance(r2_dict, float):
        r2_dict = {nparents: r2_dict for nparents in range(dag.nnodes)}

    cam_dag = CamDAG(dag._nodes, arcs=dag._arcs)
    top_order = dag.topological_sort()
    sample_dict = dict()

    # for each node, create the conditional
    node_iterator = top_order if not progress else tqdm(top_order)
    for node in node_iterator:
        parents = dag.parents_of(node)
        nparents = dag.indegree_of(node)
        parent2base = dict(zip(parents, random.choices(basis, k=nparents)))
        if nparents > 0:
            parent_vals = np.array([sample_dict[parent] for parent in parents]).T
            parent_weights = rand_weight_fn(size=nparents)
        else:
            parent_vals = np.zeros([num_monte_carlo, 0])
            parent_weights = dict()

        noise_vals = noise(size=num_monte_carlo)
        internal_variance = np.var(noise_vals)
        # print("internal variance", node, internal_variance)

        c_node = None
        b_node = np.sqrt(1/internal_variance)
        if nparents > 0:
            mean_function_no_c = partial(_cam_mean_function, c_node=1, parent_weights=parent_weights, parent2base=parent2base)
            values_from_parents = mean_function_no_c(parent_vals, parents)
            variance_from_parents = np.var(values_from_parents)

            try:
                if r2_key == "nparents":
                    desired_r2 = r2_dict[nparents]
                elif r2_key == "node":
                    desired_r2 = r2_dict[node]
            except ValueError:
                raise Exception(f"`r2_dict` does not specify a desired R^2 for nodes with {nparents} parents")
            c_node = np.sqrt(desired_r2 / variance_from_parents)
            b_node = np.sqrt((1 - desired_r2) / internal_variance)
            if np.isnan(c_node):
                raise ValueError
            # print(node, parents, variance_from_parents, parent_weights, c_node, b_node)

        mean_function = partial(_cam_mean_function, c_node=c_node, parent_weights=parent_weights, parent2base=parent2base)

        mean_vals = mean_function(parent_vals, parents)
        sample_dict[node] = mean_vals + noise_vals * b_node
        # print("variance of samples", np.var(sample_dict[node]))

        cam_dag.set_mean_function(node, mean_function)
        cam_dag.set_noise(node, create_scaled_noise_function(b_node, noise))

    return cam_dag


def create_scaled_noise_function(val, noise):
    def scaled_noise_function(size):
        return val * noise(size)
    return scaled_noise_function


# OPTION 1
# - equally predictable given parents (signal to noise ratio): internal variance \propto variance from the parents
# - compute variance of each parent. add up. set my internal noise variance \propto variance from parents
# - always keep noise variance same, scale signal coefficients

# OPTION 2
# - bound each variable

# OPTION 3


def directed_random_graph(nnodes: int, random_graph_model: Callable, size=1, as_list=False) -> Union[DAG, List[DAG]]:
    if size == 1:
        # generate a random undirected graph
        edges = random_graph_model(nnodes).edges

        # generate a random permutation
        random_permutation = np.arange(nnodes)
        np.random.shuffle(random_permutation)

        arcs = []
        for edge in edges:
            node1, node2 = edge
            node1_position = np.where(random_permutation == node1)[0][0]
            node2_position = np.where(random_permutation == node2)[0][0]
            if node1_position < node2_position:
                source = node1
                endpoint = node2
            else:
                source = node2
                endpoint = node1
            arcs.append((source, endpoint))
        d = DAG(nodes=set(range(nnodes)), arcs=arcs)
        return [d] if as_list else d
    else:
        return [directed_random_graph(nnodes, random_graph_model) for _ in range(size)]


def directed_barabasi(nnodes: int, nattach: int, size=1, as_list=False) -> Union[DAG, List[DAG]]:
    random_graph_model = lambda nnodes: barabasi_albert_graph(nnodes, nattach)
    return directed_random_graph(nnodes, random_graph_model, size=size, as_list=as_list)


def alter_weights(
        gdag: GaussDAG,
        prob_altered: float = None,
        num_altered: int = None,
        prob_added: float = None,
        num_added: int = None,
        prob_removed: float = None,
        num_removed: int = None,
        rand_weight_fn=unif_away_zero,
        rand_change_fn=unif_away_original
):
    """
    Return a copy of a GaussDAG with some of its arc weights randomly altered by `rand_weight_fn`.

    Parameters
    ----------
    gdag:
        GaussDAG
    prob_altered:
        Probability each arc has its weight altered.
    num_altered:
        Number of arcs whose weights are altered.
    prob_added:
        Probability that each missing arc is added.
    num_added:
        Number of missing arcs added.
    prob_removed:
        Probability that each arc is removed.
    num_removed:
        Number of arcs removed.
    rand_weight_fn:
        Function that returns a random weight for each new edge.
    rand_change_fn:
        Function that takes the current weight of an edge and returns the new weight.
    """
    if num_altered is None and prob_altered is None:
        raise ValueError("Must specify at least one of `prob_altered` or `num_altered`.")
    if num_added is None and prob_added is None:
        raise ValueError("Must specify at least one of `prob_added` or `num_added`.")
    if num_removed is None and prob_removed is None:
        raise ValueError("Must specify at least one of `prob_removed` or `num_removed`.")
    if num_altered + num_removed > gdag.num_arcs:
        raise ValueError(
            f"Tried altering {num_altered} arcs and removing {num_removed} arcs, but there are only {gdag.num_arcs} arcs in this DAG.")
    num_missing_arcs = comb(gdag.nnodes, 2) - gdag.num_arcs
    if num_added > num_missing_arcs:
        raise ValueError(
            f"Tried adding {num_added} arcs but there are only {num_missing_arcs} arcs missing from the DAG.")

    # GET NUMBER ADDED/CHANGED/REMOVED
    num_altered = num_altered if num_altered is not None else np.random.binomial(gdag.num_arcs, prob_altered)
    num_removed = num_removed if num_removed is not None else np.random.binomial(gdag.num_arcs, prob_removed)
    num_removed = min(num_removed, gdag.num_arcs - num_altered)
    num_added = num_added if num_added is not None else np.random.binomial(num_missing_arcs, prob_added)

    # GET ACTUAL ARCS THAT ARE ADDED/CHANGED/REMOVED
    altered_arcs = random.sample(list(gdag.arcs), num_altered)
    removed_arcs = random.sample(list(gdag.arcs - set(altered_arcs)), num_removed)
    valid_arcs_to_add = set(itr.combinations(gdag.topological_sort(), 2)) - gdag.arcs
    added_arcs = random.sample(list(valid_arcs_to_add), num_added)

    # CREATE NEW DAG
    new_gdag = gdag.copy()
    weights = gdag.arc_weights
    for i, j in altered_arcs:
        new_gdag.set_arc_weight(i, j, rand_change_fn(weights[(i, j)]))
    for i, j in removed_arcs:
        new_gdag.remove_arc(i, j)
    new_weights = rand_weight_fn(size=num_added)
    for (i, j), val in zip(added_arcs, new_weights):
        new_gdag.set_arc_weight(i, j, val)

    return new_gdag


__all__ = [
    'directed_erdos',
    'directed_erdos_with_confounders',
    'rand_weights',
    'unif_away_zero',
    'directed_barabasi',
    'directed_random_graph',
    'rand_nn_functions',
    'unif_away_original',
    'alter_weights',
    'rand_additive_basis',
    'rand_normal_wishart',
    'rand_discrete_dag',
    'rand_noisy_or_dag'
]


if __name__ == '__main__':
    d = directed_erdos(10, .5, random_order=False)
    cam_dag = rand_additive_basis(d, [np.sin])
    samples = cam_dag.sample(100)
    cond_means = cam_dag.conditional_mean(cond_values=np.ones([10, 1]), cond_nodes=[0])
