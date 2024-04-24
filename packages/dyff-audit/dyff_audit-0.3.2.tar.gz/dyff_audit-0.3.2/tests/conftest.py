# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0


def pytest_addoption(parser):
    parser.addoption("--storage_root", action="store", default=None)
