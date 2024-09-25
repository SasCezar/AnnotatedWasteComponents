import pickle
from typing import Set, Tuple, List

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from componentannotator.componentannotator import ComponentAnnotator
from loguru import logger


if __name__ == "__main__":
    ComponentAnnotator("java").annotate_projects(100)