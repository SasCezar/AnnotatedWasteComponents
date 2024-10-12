import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig

@hydra.main(config_path="../config/", config_name="main.yaml", version_base='1.3')
def run(cfg: DictConfig):
    print(f"Configuration passed to instantiate: {cfg.community.louvain}")
    louvain_algorithm = instantiate(cfg.community.louvain)
    print(f"Louvain algorithm instantiated: {louvain_algorithm}")

if __name__ == "__main__":
    run()