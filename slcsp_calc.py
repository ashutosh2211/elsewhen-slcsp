# slcsp.py

import csv
from typing import Dict, List, Tuple


class Plan:
    """Represents a health plan."""

    def __init__(self, plan_id: str, state: str, metal_level: str, rate: float, rate_area: int):
        self.plan_id = plan_id
        self.state = state
        self.metal_level = metal_level
        self.rate = rate
        self.rate_area = rate_area


class ZipCode:
    """Represents a zip code with its state, counties, and rate areas."""

    def __init__(self, zip_code: str, state: str, counties: List[Tuple[str, str]], rate_areas: List[int]):
        self.zip_code = zip_code
        self.state = state
        self.counties = counties
        self.rate_areas = rate_areas


class SlcspFinder:
    """Finds the second lowest cost silver plan for each zip code."""

    def __init__(self, plans: List[Plan], zip_codes: List[ZipCode]):
        self.plans_by_rate_area = self._group_plans_by_rate_area(plans)
        self.zip_codes = {zc.zip_code: zc for zc in zip_codes}

    def _group_plans_by_rate_area(self, plans: List[Plan]) -> Dict[int, List[Plan]]:
        plans_by_rate_area = {}
        for plan in plans:
            if plan.rate_area not in plans_by_rate_area:
                plans_by_rate_area[plan.rate_area] = []
            plans_by_rate_area[plan.rate_area].append(plan)
        return plans_by_rate_area

    def find_slcsp_for_zipcode(self, zip_code: str) -> str:
        if zip_code not in self.zip_codes:
            return ""

        zc = self.zip_codes[zip_code]

        if len(zc.rate_areas) != 1:
            return ""

        rate_area = zc.rate_areas[0]
        if rate_area not in self.plans_by_rate_area:
            return ""

        silver_plans = [p for p in self.plans_by_rate_area[rate_area] if p.metal_level == "Silver"]
        silver_plans.sort(key=lambda p: p.rate)

        if len(silver_plans) < 2:
            return ""

        return f"{silver_plans[1].rate:.2f}"

    def find_slcsp_for_all(self, zip_codes: List[str]) -> List[Tuple[str, str]]:
        return [(zc, self.find_slcsp_for_zipcode(zc)) for zc in zip_codes]


def read_plans(file_path: str) -> List[Plan]:
    plans = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            plans.append(Plan(row['plan_id'], row['state'], row['metal_level'],
                              float(row['rate']), int(row['rate_area'])))
    return plans


def read_zipcodes(file_path: str) -> List[ZipCode]:
    zip_codes = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            zip_code = row['zipcode']
            state = row['state']
            county = (row['county_code'], row['name'])
            rate_area = int(row['rate_area'])

            if zip_code not in zip_codes:
                zip_codes[zip_code] = ZipCode(zip_code, state, [], [])

            if county not in zip_codes[zip_code].counties:
                zip_codes[zip_code].counties.append(county)

            if rate_area not in zip_codes[zip_code].rate_areas:
                zip_codes[zip_code].rate_areas.append(rate_area)

    return list(zip_codes.values())


def read_slcsp(file_path: str) -> List[str]:
    zip_codes = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            zip_codes.append(row[0])
    return zip_codes


if __name__ == "__main__":
    plans = read_plans('files/plans.csv')
    zip_codes = read_zipcodes('files/zips.csv')
    slcsp_zip_codes = read_slcsp('files/slcsp.csv')

    slcsp_finder = SlcspFinder(plans, zip_codes)
    slcsp_results = slcsp_finder.find_slcsp_for_all(slcsp_zip_codes)

    print("zipcode,rate")  # Header
    for zip_code, rate in slcsp_results:
        print(f"{zip_code},{rate}")
