import asyncio
from playwright.async_api import async_playwright

user_list = ['natapionova', 'valeddm']
group_name = 'test'
throttle_delay = 0


async def invite_user_to_channel(page, username, g_name):
    # selector for '<div>' where found user resides
    div_selector = 'div.ListItem.chat-item-clickable.picker-list-item.has-ripple'

    try:
        # Group panel is opened to press 'Add user' button
        await page.click('div.MiddleHeader')
        await page.click('button[title="Add users"]')
        # username inserted into search input
        await page.fill('input#new-members-picker-search', username)
        # waiting for search result to hit the target user exactly
        await asyncio.sleep(1)
        # await page.screenshot(path="images/user_add_user.png")

        # erroneous user search result protection
        div_element = await page.query_selector(div_selector)
        if div_element is None:
            raise Exception(f"User '{username}' not added to group '{g_name}'.")
        # user is checked to be added to group
        await div_element.click()
        # await page.screenshot(path="images/user_add_ready.png")

        # Finally we add user to group
        await page.click('button[title="Add users"]')
        print(f"Successfully invited {username}")

    except Exception as e:
        print(f"Failed to invite {username}: {e}")


async def main():
    async with async_playwright() as p:
        # Create a persistent context to pass Telegram auth limits
        context = await p.chromium.launch_persistent_context(
            user_data_dir="session",
            headless=False
        )
        page = await context.new_page()

        try:
            await page.goto('https://web.telegram.org/a/', wait_until='networkidle')
            # print("Please log in to Telegram Web manually...")
            # manually authorize in Telegram
            # await asyncio.sleep(60)
            # await page.screenshot(path="images/user_authorized.png")
            print("Successfully navigated to Telegram Web.")
        except Exception as e:
            print(f"Failed to navigate: {e}")

        # Select the target group/channel
        await page.type('input[placeholder="Search"]', group_name)
        await page.click(f'text={group_name}', force=True)
        # await page.screenshot(path="images/user_group_search_1.png")

        # Target Group is found
        parent_div = page.locator('div.search-section')
        await parent_div.get_by_role('button', name=group_name, exact=True).click(force=True)
        # await page.screenshot(path="images/user_group_search_2.png")

        # Iterate over the user list and invite them to the group/channel
        for username in user_list:
            await invite_user_to_channel(page, username, g_name=group_name)
            # For testing purpose to follow Telegram restrictions
            await asyncio.sleep(throttle_delay)

        await context.close()


asyncio.run(main())
