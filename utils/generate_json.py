import os
import json

def generate_cards(base_path, rarities):
  """
  Generate a liste of cards from images in a folder

  :Args base_path:
  :Args rarities:
  :Return cards:List of all cards in a dict format
  """
  cards=[]
  card_id = 1 # Unique id for each card

  # Go through the rarities folders
  for rarity in rarities:
    rarity_path = os.path.join(base_path, rarity)

    if os.path.exists(rarity_path): # Check if folder exists
      for filename in os.listdir(rarity_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")): # Check if it is an image
          card = {
            "id" : card_id,
            "name": os.path.splitext(filename)[0], # Removes the extension from the name
            "rarity": rarity,
            "image": os.path.join(rarity_path, filename), # Path to image
            "owned": False # Default to false
          }
          cards.append(card)
          card_id += 1
  return cards

def save_cards_to_json(cards, output_file):
  """
  Save cards in json file

  :Args cards: List of cards to save
  :Args output_file: Path for json output
  """
  data = {"cards":cards}
  with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

def generate_json_file(output_file, base_path, rarities):
  """
  Function to generate the cards and save them in a json file

  :Args
    output_file: path to where json file will be generated
    base_path: path where the images are
    rarities: the names of the folders that are seperated by rarities
  """
  # Args

  # Generate cards
  cards = generate_cards(base_path, rarities)

  # Save cards in a json file
  save_cards_to_json(cards, output_file)

  print(f"Json file generated with {len(cards)} cards in {output_file}")
