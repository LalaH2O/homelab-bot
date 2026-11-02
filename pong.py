import discord


BOARD_WIDTH = 20
BOARD_HEIGHT = 10
PADDLE_HEIGHT = 3


class PongGame:
    def __init__(self, player_id: int):
        self.player_id = player_id
        self.paddle_y = (BOARD_HEIGHT - PADDLE_HEIGHT) // 2
        self.ball_x = BOARD_WIDTH // 2
        self.ball_y = BOARD_HEIGHT // 2
        self.ball_dx = 1
        self.ball_dy = 1
        self.score = 0
        self.game_over = False

    def move_paddle(self, direction: int) -> None:
        if self.game_over:
            return

        self.paddle_y = max(
            0,
            min(BOARD_HEIGHT - PADDLE_HEIGHT, self.paddle_y + direction),
        )
        self._advance_ball()

    def reset(self) -> None:
        self.__init__(self.player_id)

    def _advance_ball(self) -> None:
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if self.ball_y <= 0 or self.ball_y >= BOARD_HEIGHT - 1:
            self.ball_dy *= -1
            self.ball_y = max(0, min(BOARD_HEIGHT - 1, self.ball_y))

        if self.ball_x <= 0:
            self.ball_dx = 1
            self.ball_x = 0

        if self.ball_x >= BOARD_WIDTH - 1:
            if self.paddle_y <= self.ball_y < self.paddle_y + PADDLE_HEIGHT:
                self.ball_dx = -1
                self.ball_x = BOARD_WIDTH - 2
                self.score += 1
            else:
                self.game_over = True

    def render(self) -> str:
        rows = [[" " for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

        for y in range(self.paddle_y, self.paddle_y + PADDLE_HEIGHT):
            rows[y][BOARD_WIDTH - 1] = "▐"

        if not self.game_over:
            rows[self.ball_y][self.ball_x] = "●"

        border = "─" * (BOARD_WIDTH + 2)
        board = [f"┌{border}┐"]
        board.extend(f"│ {''.join(row)} │" for row in rows)
        board.append(f"└{border}┘")
        return "\n".join(board)


class PongView(discord.ui.View):
    def __init__(self, player_id: int):
        super().__init__(timeout=300)
        self.game = PongGame(player_id)
        self.message: discord.Message | None = None

    def embed(self) -> discord.Embed:
        if self.game.game_over:
            title = "🏓 Pong — Game Over"
            color = discord.Color.red()
            status = f"Missed! Final score: **{self.game.score}**"
        else:
            title = "🏓 Pong"
            color = discord.Color.blurple()
            status = "Use the buttons to move your paddle and return the ball."

        embed = discord.Embed(
            title=title,
            description=f"```text\n{self.game.render()}\n```",
            color=color,
        )
        embed.add_field(name="Score", value=str(self.game.score), inline=True)
        embed.add_field(name="Status", value=status, inline=True)
        embed.set_footer(text="Only the player who started this game can use these buttons.")
        return embed

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.game.player_id:
            await interaction.response.send_message(
                "This is someone else's Pong game.",
                ephemeral=True,
            )
            return False
        return True

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        if self.message is not None:
            await self.message.edit(view=self)

    async def _move(self, interaction: discord.Interaction, direction: int) -> None:
        self.game.move_paddle(direction)
        if self.game.game_over:
            self.up.disabled = True
            self.down.disabled = True
        await interaction.response.edit_message(embed=self.embed(), view=self)

    @discord.ui.button(label="Up", emoji="⬆️", style=discord.ButtonStyle.primary)
    async def up(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self._move(interaction, -1)

    @discord.ui.button(label="Down", emoji="⬇️", style=discord.ButtonStyle.primary)
    async def down(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await self._move(interaction, 1)

    @discord.ui.button(label="Reset", emoji="🔄", style=discord.ButtonStyle.secondary)
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.game.reset()
        self.up.disabled = False
        self.down.disabled = False
        await interaction.response.edit_message(embed=self.embed(), view=self)


async def start_game(channel: discord.abc.Messageable, player_id: int) -> discord.Message:
    view = PongView(player_id)
    message = await channel.send(embed=view.embed(), view=view)
    view.message = message
    return message
