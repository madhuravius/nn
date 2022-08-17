from nn.sources.view import generate_sources_table


async def get_and_show_sources(
    debug: bool,
):
    _, table = await generate_sources_table(debug)
    return table
