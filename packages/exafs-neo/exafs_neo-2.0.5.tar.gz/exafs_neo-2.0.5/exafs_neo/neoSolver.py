from exafs_neo.exafs_pop import NeoPopulations
from exafs_neo.neoPars import NeoPars


class NeoSolverBase:
    def __init__(self, exafs_pars, logger):
        """
        Initialize the selector base class
        :param exafs_pars:
        :param logger:
        """
        self.logger = logger
        self.exafs_pars = exafs_pars

        self.sol_list = []

    def select(self, pops):
        pass

    def __str__(self):
        # return f"Top Percentage: {100 * self.nBest_Percent}%, Lucky: {100 * self.nLucky_Percent}%"
        return f"Neo Solver"


class NeoSolver_GA(NeoSolverBase):
    """
    Standard GA algorithm solver
    """

    def __init__(self, exafs_pars, logger):
        super().__init__(exafs_pars, logger)
        self.solver_type = 0
        self.solver_operator = "Genetic Algorithm"

    def solve(self, pops):
        pass


class NeoSolver_GA_Rechenberg(NeoSolverBase):
    """
    Standard GA with Rechenberg addition
    """

    def __init__(self, exafs_pars, logger):
        super().__init__(exafs_pars, logger)
        self.solver_type = 1
        self.solver_operator = "Genetic Algorithm with Rechenberg"

    def solve(self, pops):
        pass


class NeoSolver:

    def __init__(self, logger=None):
        """
        Neo Selector
        :param NeoLogger logger: logger for Neo
        """
        self.solver_operator = None
        self.logger = logger
        self.solver_type = None
        self.exafs_pars = None

    def initialize(self, exafs_pars):
        """
        Initialize the Selector
        :param exafs_pars:
        :return:
        """
        self.exafs_pars = exafs_pars
        # self.solver_type = exafs_pars.selPars.selOpt
        self.solver_type = exafs_pars.solPars.solOpt
        if self.solver_type == 0:
            self.solver_operator = NeoSolver_GA(exafs_pars, logger=self.logger)
        elif self.solver_type == 1:
            self.solver_operator = NeoSolver_GA_Rechenberg(exafs_pars, logger=self.logger)
        else:
            self.solver_operator = NeoSolverBase(exafs_pars, logger=self.logger)
            raise ValueError("Invalid selector type, returning standard selector type.")

    def solve(self, pops):
        """
        Perform the actual selection
        :param NeoPopulation pops:  
        :return:
        """
        if self.solver_operator is None:
            raise ValueError("Selector is not initialized")
        else:
            return self.solver_operator.select(pops)

    def __str__(self):
        if self.solver_operator is None:
            return "None Mutator selected"
        else:
            return f"Selector Type: {self.solver_type}, {self.solver_operator}"


if __name__ == "__main__":
    inputs_pars = {'data_file': '../path_files/Cu/cu_10k.xmu', 'output_file': '',
                   'feff_file': '../path_files/Cu/path_75/feff', 'kmin': 0.95,
                   'kmax': 9.775,
                   'kweight': 3.0, 'pathrange': [1, 2, 3, 4, 5],
                   'deltak': 0.05, 'rbkg': 1.1, 'bkgkw': 1.0, 'bkgkmax': 15.0,
                   'solver_type': 1}
    exafs_NeoPars = NeoPars()
    exafs_NeoPars.read_inputs(inputs_pars)

    neo_population = NeoPopulations(exafs_NeoPars)
    neo_population.initialize_populations()

    exafs_selector = NeoSolver()
    exafs_selector.initialize(exafs_pars=exafs_NeoPars)
    exafs_selector.solve(neo_population)
    print(exafs_selector)
