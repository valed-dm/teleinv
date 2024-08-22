import asyncio
from playwright.async_api import async_playwright

user_list = ['natapionova', 'valeddm']
group_name = 'test'
throttle_delay = 5


async def invite_user_to_channel(page, username):
    try:
        await page.click('button[title="Add users"]')
        await page.fill('input#new-members-picker-search', username)
        # await page.wait_for_selector('div.ListItem-button')
        # input("Press Enter to continue...")
        # await page.screenshot(path="images/user_add_user.png")

        # await page.screenshot(path="images/user_add_ready.png")
        # input("Press Enter to continue...")
        await page.click('div.ListItem-button')

        await page.click('button[title="Add users"]')
        print(f"Successfully invited {username}")

    except Exception as e:
        print(f"Failed to invite {username}: {e}")


async def main():
    async with async_playwright() as p:
        # Create a persistent context
        context = await p.chromium.launch_persistent_context(
            user_data_dir="session",
            headless=False
        )
        page = await context.new_page()

        try:
            await page.goto('https://web.telegram.org/', wait_until='networkidle')
            # print("Please log in to Telegram Web manually...")
            # manually authorize in Telegram
            # await asyncio.sleep(60)
            # await page.screenshot(path="images/user_authorized.png")
            print("Successfully navigated to Telegram Web.")
            input("Press Enter to continue...")
        except Exception as e:
            print(f"Failed to navigate: {e}")

        # Select the target group/channel
        await page.type('input.input-field-input', group_name)
        await page.click(f'text={group_name}', force=True)
        await page.fill('input.input-field-input', '')
        # await page.screenshot(path="images/user_group_search_1.png")
        # input("Press Enter to continue...")

        await page.click('div.ListItem.chat-item-clickable.search-result')
        # await page.screenshot(path="images/user_group_search_2.png")

        # Iterate over the user list and invite them to the group/channel
        for username in user_list:
            await invite_user_to_channel(page, username)
            await asyncio.sleep(throttle_delay)

        await context.close()


# Run the script
asyncio.run(main())
