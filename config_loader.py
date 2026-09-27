import yaml


def load_config():

    with open("config/config.yaml", "r") as file:
        config = yaml.safe_load(file)

    return config

#temp test
if __name__ == "__main__":

    config = load_config()

    print(config)