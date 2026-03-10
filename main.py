import argparse
import yaml

from src.simulation import ChiralTwin

# Command: python main.py config.yaml -ic achiral_majority_64

def main():

    parser = argparse.ArgumentParser(
      description = "Run homochirality cellular automaton digital twin with specified configuration"
      )
    parser.add_argument("config", 
	    help = "Path to the .yaml configuration file"
	    )
    parser.add_argument("-ic",
        default = "achiral_majority",
        help = "Name of the initial condition, no extension"
    )
    args = parser.parse_args()

    # Initial condition array
    array = "data/initial-conditions/" + args.ic + ".npy"

    # All other parameters
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    # Run!
    twin = ChiralTwin(array, config)
    twin.timeEvolution()

if __name__ == "__main__":

    # Header

    print("""
          ▄▄                                             
        ▄█▀▀█▄                                   █▄      
        ██  ██   ▄              ▄          ▄    ▄██▄     
        ██▀▀██   ███▄███▄ ▄▀▀█▄ ████▄▄▀▀█▄ ████▄ ██ ▄▀▀█▄
      ▄ ██  ██   ██ ██ ██ ▄█▀██ ██   ▄█▀██ ██ ██ ██ ▄█▀██
      ▀██▀  ▀█▄█▄██ ██ ▀█▄▀█▄██▄█▀   ▀█▄██▄██ ▀█▄██▄▀█▄██   
                          is working...
    """)

    main()

                                                                                                   

                                                                                                                                           
