def format_subreddit_urls(urls):
    response = ""
    for idx, url in enumerate(urls, 1):
        response += f"{idx}: {url}\n\n"
    return response
