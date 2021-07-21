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
    # the `var cards` line is in `script` 61
    # the `var cards` line is on line 6
    # split between the assignment
    # strip the leading space, and trailing semi-colon
    raw_cards = soup.find_all('script')[61].string.split('\n')[6].split('=')[1].lstrip().rstrip(';')
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

    output_filename = f"{now}_card_dump.csv"
    # print(cards)
    with open(os.path.join(args.output_dir, output_filename), 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=cards["headers"])
        writer.writeheader()
        for card in cards["data"]:
            writer.writerow(dict(zip(cards["headers"], card)))



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output-dir", help="Directory to put CSV", required=True)

    args = parser.parse_args()
    main(args)
