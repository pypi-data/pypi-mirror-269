import asyncio

from codeinterpreterapi_yayi import CodeInterpreterSession, File


def test_codebox() -> None:
    session = CodeInterpreterSession()
    assert run_sync(session), "Failed to run sync CodeInterpreterSession remotely"
    session = CodeInterpreterSession()
    assert asyncio.run(
        run_async(session)
    ), "Failed to run async CodeInterpreterSession remotely"


def test_localbox() -> None:
    # TODO(adamzou): Ideally, we don't need to specify custom packages.
    # The agent should be able to install the packages needed automatically.
    # We may need to change the way we install packages in CodeBox from "!pip" to "% pip",
    # and also to use an LLM model that can handle the installation process of packages better.
    session = CodeInterpreterSession(
        custom_packages=["openpyxl", "yfinance", "scikit-learn"], local=True
    )
    assert run_sync(session), "Failed to run sync CodeInterpreterSession locally"
    session = CodeInterpreterSession(
        custom_packages=["openpyxl", "yfinance", "scikit-learn"], local=True
    )
    assert asyncio.run(
        run_async(session)
    ), "Failed to run async CodeInterpreterSession locally"


def run_sync(session: CodeInterpreterSession) -> bool:
    try:
        assert session.start() == "started"
        assert (
            "3.1"
            in session.generate_response(
                "Compute pi using Monte Carlo simulation in Python and show me the result."
            ).content
        )

        assert (
            ".xlsx"
            in session.generate_response(
                "Convert this csv file to excel.",
                files=[File.from_path("examples/assets/iris.csv")],
            )
            .files[0]
            .name
        )

        assert (
            ".png"
            in session.generate_response(
                "Plot the current stock price of Tesla.",
            )
            .files[0]
            .name
        )

        assert (
            ".joblib"
            in session.generate_response(
                "Train a simple linear regression model on 'TV advertising' and \
                'Sales' in this csv file and return the model in joblib format.",
                files=[File.from_path("examples/assets/advertising.csv")],
            )
            .files[0]
            .name
        )

    finally:
        assert session.stop() == "stopped"

    return True


async def run_async(session: CodeInterpreterSession) -> bool:
    try:
        assert (await session.astart()) == "started"
        assert (
            "3.1"
            in (
                await session.agenerate_response(
                    "Compute pi using Monte Carlo simulation in Python and show me the result."
                )
            ).content
        )

        assert (
            ".xlsx"
            in (
                await session.agenerate_response(
                    "Convert this csv file to excel.",
                    files=[File.from_path("examples/assets/iris.csv")],
                )
            )
            .files[0]
            .name
        )

        assert (
            ".png"
            in (
                await session.agenerate_response(
                    "Plot the current stock price of Tesla.",
                )
            )
            .files[0]
            .name
        )

        assert (
            ".joblib"
            in (
                await session.agenerate_response(
                    "Train a simple linear regression model on 'TV advertising' and \
                'Sales' in this csv file and return the model in joblib format.",
                    files=[File.from_path("examples/assets/advertising.csv")],
                )
            )
            .files[0]
            .name
        )

    finally:
        assert await session.astop() == "stopped"

    return True


if __name__ == "__main__":
    test_codebox()
    test_localbox()
