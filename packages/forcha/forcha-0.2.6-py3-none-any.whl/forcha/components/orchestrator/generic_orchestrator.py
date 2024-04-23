import copy
from multiprocessing import Pool

import numpy as np
from torch import nn
import datasets 

from forcha.components.nodes.federated_node import FederatedNode
from forcha.models.federated_model import FederatedModel
from forcha.utils.computations import Aggregators
from forcha.utils.loggers import Loggers
from forcha.utils.orchestrations import sample_nodes, train_nodes
from forcha.components.settings.settings import Settings
from forcha.utils.debugger import log_gpu_memory
from forcha.utils.helpers import Helpers
from forcha.utils.handlers import save_csv_file, save_model_metrics, save_training_metrics


# set_start_method set to 'spawn' to ensure compatibility across platforms.
from multiprocessing import set_start_method
set_start_method("spawn", force=True)


class Orchestrator():
    """Orchestrator is a central object necessary for performing the simulation.
        It connects the nodes, maintain the knowledge about their state and manages the
        multithread pool. generic_orchestrator.orchestrator is a parent to all more
        specific orchestrators."""


    def __init__(
        self, 
        settings: Settings,
        number_of_workers: int = 20,
        **kwargs
        ) -> None:
        """Orchestrator is initialized by passing an instance
        of the Settings object. Settings object contains all the relevant configurational
        settings that an instance of the Orchestrator object may need to complete the simulation.
        
        Attributes
        ----------
        settings: Forcha.settings.Settings
            A settings object containing all the settings used during the simulation.
        net: nn.Module
            A template of the neural network architecture that is loaded into FederatedModel.
        central_model: forcha.models.federated_model.FederatedModel
            A FederatedModel object attached to the orchestrator.
        orchestrator_logger: forcha.utils.loggers.Loggers
            A pre-configured logger attached to the Orchestrator.
        validation_data: datasets.arrow_dataset.Dataset
            A datasets.arrow_dataset.Dataset with validation data for the Orchestrator.
        full_debug: Bool
            A boolean flag enabling full debug mode of the orchestrator (default to False).
        batch_job: Bool
            A boolean flag diasbling simultaneous training of the clients (default to False).
        (optional) batch: int
            If batch_job is set to True, this will be a number of clients allowed
            to train simultaneously.
        parallelization: Bool
            A boolean flag enabling parallelization of certain operations (default to False)
        generator: np.random.default_rng
            A random number generator attached to the Orchestrator.
        
        Parameters
        ----------
        settings : Settings
            An instance of the settings object cotaining all the settings 
            of the orchestrator.
        **kwargs : dict, optional
            Extra arguments to enable selected features of the Orchestrator.
            passing full_debug to **kwargs, allow to enter a full debug mode.
       
       Returns
       -------
       None
       """
        self.settings = settings
        self.network = [] # Network of available nodes (connected and disconnected)
        # Special option to enter a full debug mode.
        if kwargs.get("full_debug"):
            self.full_debug = True
        else:
            self.full_debug = False
        # Batch job enabled or disabled
        if kwargs.get("batch_job"):
            self.batch_job = True
            self.batch = kwargs["batch"]
        else:
            self.batch_job = False
        # Parallelization enabled or disabled
        if kwargs.get("parallelization"):
            self.parallelization = True
        else:
            self.parallelization = False
        self.number_of_workers = number_of_workers
        self.orchestrator_logger = Loggers.orchestrator_logger()
        
        # Initialization of the generator object    
        self.generator = np.random.default_rng(self.settings.simulation_seed)
    
    
    def prepare_orchestrator(
        self, 
        model: nn,
        validation_data: datasets.arrow_dataset.Dataset,
        ) -> None:
        """Loads the orchestrator's test data and creates an instance
        of the Federated Model object that will be used throughout the training.
        
        Parameters
        ----------
        validation_data : datasets.arrow_dataset.Dataset:
            Validation dataset that will be used by the Orchestrator.
        model : torch.nn
            Model architecture that will be used throughout the training.
        
        Returns
        -------
        None
        """
        self.validation_data = [validation_data]
        self.central_net = model
        self.central_model = FederatedModel(
            settings = self.settings,
            net=model,
            local_dataset=self.validation_data,
            node_name='orchestrator')
    
    
    def prepare_training(
        self,
        nodes_data: list[datasets.arrow_dataset.Dataset,
                         datasets.arrow_dataset.Dataset]
        ) -> None:
        """Prepares all the necessary elements of the training, including nodes and helpers.
        Must be run before the train_protocol method is invoked.
        
        Parameters
        ----------
        nodes_data: list[datasets.arrow_dataset.Dataset, datasets.arrow_dataset.Dataset] 
            A list containing train set and test set
            wrapped in a hugging face arrow_dataset.Dataset containers.

        Returns
        -------
        None
        """
        
        self.iterations = self.settings.global_epochs
        self.nodes_number = self.settings.number_of_nodes
        self.sample_size = self.settings.sample_size
        self.nodes_list = [node for node in range(self.nodes_number)]
        model_list = [copy.deepcopy(self.central_net) for _ in range(self.nodes_number)]
        nodes = [FederatedNode(node_id, 
                                    self.settings,
                                    model=model,
                                    data=node_data,
                                    save_model=self.settings.save_nodes_models,
                                    save_path=self.settings.nodes_model_path,
                                    seed=self.settings.simulation_seed) 
                      for node_id, model, node_data in zip(self.nodes_list, model_list, nodes_data)]
        self.network = nodes
    
    
    def update_connectivity(self,
                            iteration:int):
        for node in self.network:
            node.update_state(iteration=iteration)
        connected = [node for node in self.network if node.state == 1]
        return connected


    def train_protocol(self) -> None:
        """Performs a full federated training according to the initialized
        settings. The train_protocol of the generic_orchestrator.Orchestrator
        follows a classic FedAvg algorithm - it averages the local weights 
        and aggregates them taking a weighted average.
        SOURCE: Communication-Efficient Learning of
        Deep Networks from Decentralized Data, H.B. McMahan et al.

        Parameters
        ----------
        
        Returns
        -------
        int
            Returns 0 on the successful completion of the training."""
        # BEGINING OF TRAINING
        ########################################################
        ########################################################
        ########################################################
        
        # TRAINING PHASE ----- FEDAVG
        for iteration in range(self.iterations):
            # BEGINING OF ITERATION
            ########################################################
            ########################################################
            self.orchestrator_logger.info(f"Iteration {iteration}")
            
            ########################################################
            # FEDAVG - INIT PHASE
            weights = {}
            training_results = {}
            # Checking for connectivity
            connected_nodes = [node for node in self.network]
            self.orchestrator_logger.info(f"Iteration {iteration}, dispatching nodes to connected clients.")
            for node in connected_nodes:
                node.model.update_weights(copy.deepcopy(self.central_model.get_weights()))
            ########################################################
            
            ########################################################
            # FEDAVG - SAMPLING PHASE
            sampled_nodes = sample_nodes(
                nodes = connected_nodes, 
                sample_size = self.sample_size,
                generator = self.generator
                ) # SAMPLING FUNCTION
            ########################################################
            
            ########################################################
            # FEDAVG - TRAINING PHASE
            # FEDAVG OPTION I: BATCH TRAINING
            if self.batch_job:
                self.orchestrator_logger.info(f"Entering batched job, size of the batch {self.batch}")
                for batch in Helpers.chunker(sampled_nodes, size=self.batch):
                    with Pool(len(list(batch))) as pool:
                        results = [pool.apply_async(train_nodes, (node, iteration, 'weights')) for node in batch]
                        for result in results:
                            node_id, model_weights, loss_list, accuracy_list = result.get()
                            weights[node_id] = model_weights
                            training_results[node_id] = {
                                "iteration": iteration,
                                "node_id": node_id,
                                "loss": loss_list[-1], 
                                "accuracy": accuracy_list[-1]
                                }
            # FEDAVG OPTION II: BATCH TRAINING
            else:
                with Pool(self.sample_size) as pool:
                    results = [pool.apply_async(train_nodes, (node, iteration)) for node in sampled_nodes]
                    for result in results:
                            node_id, model_weights, loss_list, accuracy_list = result.get()
                            weights[node_id] = model_weights
                            training_results[node_id] = {
                                "iteration": iteration,
                                "node_id": node_id,
                                "loss": loss_list[-1], 
                                "accuracy": accuracy_list[-1]
                                }
            ########################################################
            
            ########################################################
            # FEDAVG - TESTING RESULTS BEFORE THE MODEL UPDATE PHASE
            if self.settings.save_training_metrics:
                save_training_metrics(
                    file = training_results,
                    saving_path = self.settings.results_path,
                    file_name = "training_metrics.csv"
                    )
            # METRICS: TEST RESULTS ON NODES (TRAINED MODEL)
                for node in sampled_nodes:
                    save_model_metrics(
                        iteration = iteration,
                        model = node.model,
                        logger = self.orchestrator_logger,
                        saving_path = self.settings.results_path,
                        file_name = 'local_model_on_nodes.csv'
                        )
            ########################################################
            
            ########################################################
            # FEDAVG: AGGREGATING AND CENTRAL UPDATE
            avg = Aggregators.compute_average(copy.deepcopy(weights)) # AGGREGATING FUNCTION
            self.central_model.update_weights(copy.deepcopy(avg))
            ########################################################
            
            ########################################################
            # FEDAVG - UPDATING THE NODES AND SAVE RESULTS
            for node in connected_nodes:
                node.model.update_weights(copy.deepcopy(avg))
            self.central_model.update_weights(copy.deepcopy(avg))
            if self.settings.save_training_metrics:
                save_model_metrics(
                    iteration = iteration,
                    model = self.central_model,
                    logger = self.orchestrator_logger,
                    saving_path = self.settings.results_path,
                    file_name = "global_model_on_orchestrator.csv"
                )
                for node in connected_nodes:
                    save_model_metrics(
                        iteration = iteration,
                        model = node.model,
                        logger = self.orchestrator_logger,
                        saving_path = self.settings.results_path,
                        file_name = "global_model_on_nodes.csv")
            ########################################################
            
            if self.full_debug == True:
                log_gpu_memory(iteration=iteration)
            ########################################################
            ########################################################
            # END OF ITERATION
                            
        ########################################################
        self.orchestrator_logger.critical("Training complete")
        return 0
                        
