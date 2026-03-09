import argparse
import yaml
from src.simulation import DigitalTwin

def main():

    # Configuration file
    parser = argparse.ArgumentParser(
	    description="Run Chiral CA Simulation"
	    )
    parser.add_argument("config", 
	    help="Path to the .yaml configuration file"
	    )
    args = parser.parse_args()

    # Parameters
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    # Initialize and run the digital twin
    twin = DigitalTwin(config)
    twin.run()

if __name__ == "__main__":
    main()
