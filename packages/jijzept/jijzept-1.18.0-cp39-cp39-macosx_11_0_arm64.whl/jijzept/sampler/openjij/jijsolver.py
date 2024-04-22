from __future__ import annotations

import typing as typ

from dataclasses import dataclass

import jijmodeling as jm

from jijzept.entity.schema import SolverType
from jijzept.response import JijModelingResponse
from jijzept.sampler.base_sampler import (
    JijZeptBaseSampler,
    ParameterSearchParameters,
    check_kwargs_against_dataclass,
    merge_params_and_kwargs,
    sample_instance,
    sample_model,
)
from jijzept.type_annotation import FixedVariables, InstanceData

T = typ.TypeVar("T")


@dataclass
class JijSolverParameters:
    """Manage Parameters for using JijSolver's WeightedLS.

    Attributes:
        num_iters (int): The number of iterations (each iteration consists of SFSA, SFLS, MFLS, and update of the weights).
        time_limit_msec (int): How long does the solver take for each SA (LS) part (in units of millisecond).
        count (int): The number of iterations during each SA (LS) part.
    """
    num_iters: int = 4
    time_limit_msec: typ.Optional[float] = None
    count: typ.Optional[int] = None


class JijSolver(JijZeptBaseSampler):
    jijmodeling_solver_type = SolverType(queue_name="openjijsolver", solver="JijSolverV2")

    def sample_model(
        self,
        model: jm.Problem,
        feed_dict: InstanceData,
        fixed_variables: FixedVariables = {},
        parameters: JijSolverParameters = JijSolverParameters(time_limit_msec=2000),
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str | None = None,
        **kwargs,
    ) -> JijModelingResponse:
        """Sample using JijSolver.

        To configure the solver, instantiate the `JijSolverParameters` class and pass the instance to the `parameters` argument.

        Args:
            model (jm.Problem): Mathematical expression of JijModeling.
            feed_dict (dict[str, int | float | numpy.integer | numpy.floating | numpy.ndarray | list]): The actual values to be assigned to the placeholders.
            fixed_variables (dict[str, dict[tuple[int, ...], int]]): dictionary of variables to fix.
            parameters (JijSAParameters | None, optional): defaults JijSolverParameters().
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 600 will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool, optional): Synchronous mode.
            queue_name (Optional[str], optional): Queue name.
            **kwargs: Parameters of jijsolver. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

        Returns:
            JijModelingResponse: Stores minimum energy samples and other information.

        Examples:
            ```python
            import jijzept as jz
            import jijmodeling as jm

            n = jm.Placeholder('n')
            x = jm.BinaryVar('x', shape=(n,))
            d = jm.Placeholder('d', ndim=1)
            i = jm.Element("i", belong_to=n)
            problem = jm.Problem('problem')
            problem += jm.sum(i, d[i] * x[i])

            sampler = jz.JijSolver(config='config.toml')
            response = sampler.sample_model(problem, feed_dict={'n': 5, 'd': [1,2,3,4,5]})
            ```
        """
        check_kwargs_against_dataclass(kwargs, JijSolverParameters)
        param_dict = merge_params_and_kwargs(parameters, kwargs, JijSolverParameters)

        para_search_params = ParameterSearchParameters()

        if queue_name is None:
            queue_name = self.jijmodeling_solver_type.queue_name

        sample_set = sample_model(
            client=self.client,
            solver=self.jijmodeling_solver_type.solver,
            queue_name=queue_name,
            problem=model,
            instance_data=feed_dict,
            fixed_variables=fixed_variables,
            parameter_search_parameters=para_search_params,
            max_wait_time=max_wait_time,
            sync=sync,
            **param_dict,
        )
        return sample_set

    def sample_instance(
        self,
        instance_id: str,
        fixed_variables: FixedVariables = {},
        parameters: JijSolverParameters = JijSolverParameters(time_limit_msec=2000),
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str | None = None,
        system_time: jm.SystemTime = jm.SystemTime(),
        **kwargs,
    ) -> JijModelingResponse:
        """Sample using JijSolver.

        To configure the solver, instantiate the `JijSolverParameters` class and pass the instance to the `parameters` argument.

        Args:
            instance_id (str): The ID of the uploaded instance.
            fixed_variables (dict[str, dict[tuple[int, ...], int]]): dictionary of variables to fix.
            parameters (JijSAParameters | None, optional): defaults JijSolverParameters().
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 600 will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool, optional): Synchronous mode.
            queue_name (Optional[str], optional): Queue name.
            **kwargs: Parameters of jijsolver. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

        Returns:
            JijModelingResponse: Stores minimum energy samples and other information.

        Examples:
            ```python
            import jijzept as jz
            import jijmodeling as jm

            n = jm.Placeholder('n')
            x = jm.BinaryVar('x', shape=(n,))
            d = jm.Placeholder('d', ndim=1)
            i = jm.Element("i", belong_to=n)
            problem = jm.Problem('problem')
            problem += jm.sum(i, d[i] * x[i])

            # initialize sampler
            sampler = jz.JijSolver(config='config.toml')

            # upload instance
            instance_id = sampler.upload_instance(problem, {'n': 5, 'd': [1,2,3,4,5]})

            # sample uploaded instance
            sample_set = sampler.sample_instance(instance_id)
            ```
        """
        check_kwargs_against_dataclass(kwargs, JijSolverParameters)
        param_dict = merge_params_and_kwargs(parameters, kwargs, JijSolverParameters)

        para_search_params = ParameterSearchParameters()

        if queue_name is None:
            queue_name = self.jijmodeling_solver_type.queue_name

        sample_set = sample_instance(
            client=self.client,
            solver=self.jijmodeling_solver_type.solver,
            queue_name=queue_name,
            instance_id=instance_id,
            fixed_variables=fixed_variables,
            parameter_search_parameters=para_search_params,
            max_wait_time=max_wait_time,
            sync=sync,
            system_time=system_time,
            **param_dict,
        )

        return sample_set
