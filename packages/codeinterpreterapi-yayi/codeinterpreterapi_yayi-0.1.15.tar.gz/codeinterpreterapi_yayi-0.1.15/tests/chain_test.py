from codeinterpreterapi_yayi.chains import remove_download_link, get_file_modifications
from codeinterpreterapi_yayi import CodeInterpreterSession

llm = CodeInterpreterSession()._choose_llm()


def test_remove_download_link() -> None:
    example = (
        "I have created the plot to your dataset.\n\n"
        "Link to the file [here](sandbox:/plot.png)."
    )
    assert (
        remove_download_link(example, llm).strip()
        == "I have created the plot to your dataset."
    )


def test_get_file_modifications() -> None:
    base_code = """
        import matplotlib.pyplot as plt

        x = list(range(1, 11))
        y = [29, 39, 23, 32, 4, 43, 43, 23, 43, 77]

        plt.plot(x, y, marker='o')
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.title('Data Plot')
        """
    code_with_mod = base_code + "\nplt.savefig('plot.png')"

    code_no_mod = base_code + "\nplt.show()"

    assert get_file_modifications(code_with_mod, llm) == ["plot.png"]
    assert get_file_modifications(code_no_mod, llm) == []


if __name__ == "__main__":
    # test_remove_download_link()
    test_get_file_modifications()
