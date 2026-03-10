import argparse
import yaml
from src.simulation import DigitalTwin

def main():

    parser = argparse.ArgumentParser(
      description = "Run homochirality cellular automaton digital twin with specified configuration"
      )
    parser.add_argument("config", 
	    help = "Path to the .yaml configuration file"
	    )
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    twin = DigitalTwin(config)
    twin.run()

if __name__ == "__main__":
    main()


# ASCII arts                                                                                                        
#      ▄▄                                             
#    ▄█▀▀█▄                                   █▄      
#    ██  ██   ▄              ▄          ▄    ▄██▄     
#    ██▀▀██   ███▄███▄ ▄▀▀█▄ ████▄▄▀▀█▄ ████▄ ██ ▄▀▀█▄
#  ▄ ██  ██   ██ ██ ██ ▄█▀██ ██   ▄█▀██ ██ ██ ██ ▄█▀██
#  ▀██▀  ▀█▄█▄██ ██ ▀█▄▀█▄██▄█▀  ▄▀█▄██▄██ ▀█▄██▄▀█▄██
                                                    
                                                                                                                                           
