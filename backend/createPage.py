def template1(name, products):
    astro_content = f"""---
    import Layout from "../../../../layouts/Layout.astro"
    ---
    <Layout title="{name}">
        <h1>{name}</h1>
    </Layout>
    """
    return astro_content