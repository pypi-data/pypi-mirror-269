import pytest

from iwashi import tree


@pytest.mark.asyncio
async def test_youtube_tree():
    result = await tree("https://www.youtube.com/@SebastianLague")
    assert result, "No result found"
    link_list = result.to_list()
    assert len(link_list) == 6, f"Expected 1 result, got {len(link_list)}"
