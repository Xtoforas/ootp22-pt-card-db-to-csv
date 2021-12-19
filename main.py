#!/usr/bin/env python3

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import json
import os
import requests

def main(args):

    now = datetime.now().strftime("%Y%m%d_%H_%M_%S")
    url = "https://www.ootpdevelopments.com/perfect-team-22-baseball-card-list/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    # the `var cards` line is in `script` 62
    # the `var cards` line is on line 6
    # split between the assignment
    # strip the leading space, and trailing semi-colon

    raw_cards = soup.find_all('script')[62].string.split('\n')[6].split('=')[1].lstrip().rstrip(';')
    cards = json.loads('{{"data":{}}}'.format(raw_cards))
    cards["headers"] = [
        "CardTitle",
        "Card Value",
        "Year",
        "Last Name",
        "First Name",
        "Bats",
        "Throws",
        "Position",
        "Role",
        "Contact",
        "Gap",
        "Power",
        "Eye",
        "AvoidK",
        "Contact vL",
        "Gap vL",
        "Power vL",
        "Eye vL",
        "AvK vL",
        "Contact vR",
        "Gap vR",
        "Power vR",
        "Eye vR",
        "AvK vR",
        "Speed",
        "Stealing",
        "Baserunning",
        "Sac Bunt",
        "Bunt for Hit",
        "Stuff",
        "Movement",
        "Control",
        "Stuff vL",
        "Movement vL",
        "Control vL",
        "Stuff vR",
        "Movement vR",
        "Control vR",
        "Faseball Rating",
        "Changeup Rating",
        "Curveball Rating",
        "Slider Rating",
        "Sinker Rating",
        "Splitter Rating",
        "Cutter Rating",
        "Forkball Rating",
        "Circle Change Rating",
        "Screwball Rating",
        "Knuckle Curve Rating",
        "Knuckleball Rating",
        "Arm Endurance",
        "Hold Runner",
        "GB Tendency",
        "Velocity",
        "Arm Slot",
        "Infield Range",
        "Infield Error",
        "Infield Arm",
        "Infield Doubleplay",
        "Catcher Ability",
        "Catcher Arm",
        "Outfield Range",
        "Outfiled Error",
        "Outfiled Arm",
        "Pitcher Fielding",
        "Catcher Fielding",
        "1B Fielding",
        "2B Fielding",
        "3B Fielding",
        "SS Fielding",
        "LF Fielding",
        "CF Fielding",
        "RF Fielding",
        "Height",
        "Card ID",
        "Team"
    ]

    hand_dict = {
        1: "R",
        2: "L",
        3: "S"
    }

    fielding_dict = {
        1: "P",
        2: "C",
        3: "1B",
        4: "2B",
        5: "3B",
        6: "SS",
        7: "LF",
        8: "CF",
        9: "RF",
        10: "DH"
    }

    role_dict = {
        11: "SP",
        12: "RP",
        13: "CL"
    }

    batters_output_filename = f"{now}_card_dump_batters.csv"
    pitchers_output_filename = f"{now}_card_dump_pitchers.csv"
    # print(cards)
    with open(os.path.join(args.output_dir, batters_output_filename), 'w') as batters_csv_file:
        with open(os.path.join(args.output_dir, pitchers_output_filename), 'w') as pitchers_csv_file:
            batters_writer = csv.DictWriter(batters_csv_file, fieldnames=cards["headers"])
            batters_writer.writeheader()
            pitchers_writer = csv.DictWriter(pitchers_csv_file, fieldnames=cards["headers"])
            pitchers_writer.writeheader()
            for card in cards["data"]:
                throwing_index = cards["headers"].index('Throws')
                card[throwing_index] = hand_dict[card[throwing_index]]

                hitting_index = cards["headers"].index('Bats')
                card[hitting_index] = hand_dict[card[hitting_index]]

                position_index = cards["headers"].index("Position")
                card[position_index] = fielding_dict[card[position_index]]

                role_index = cards["headers"].index("Role")
                if card[role_index] == 0:
                    card[role_index] = card[position_index]
                else:
                    card[role_index] = role_dict[card[role_index]]

                if card[position_index] == "P":
                    pitchers_writer.writerow(dict(zip(cards["headers"], card)))
                else:
                    batters_writer.writerow(dict(zip(cards["headers"], card)))



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output-dir", help="Directory to put CSV", required=True)

    args = parser.parse_args()
    main(args)
