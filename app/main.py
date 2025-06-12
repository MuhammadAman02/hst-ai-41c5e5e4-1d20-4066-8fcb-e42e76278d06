from nicegui import ui, events
import asyncio
from app.game.engine import GameEngine
from app.config import settings

# Global game instance
game = GameEngine()

@ui.page('/')
async def main_page():
    ui.add_head_html('''
        <style>
            body { 
                margin: 0; 
                padding: 0; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                font-family: 'Arial', sans-serif;
                overflow: hidden;
            }
            .game-container {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
            }
            .game-canvas {
                border: 3px solid #fff;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                background: linear-gradient(to bottom, #87CEEB 0%, #98FB98 100%);
            }
            .game-ui {
                position: absolute;
                top: 20px;
                left: 20px;
                color: white;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                z-index: 10;
            }
            .game-over-screen {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0,0,0,0.8);
                color: white;
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                z-index: 20;
            }
            .controls-info {
                position: absolute;
                bottom: 20px;
                left: 20px;
                color: white;
                font-size: 14px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            }
        </style>
    ''')
    
    with ui.column().classes('game-container'):
        # Game title
        ui.label('🚇 SUBWAY SURFERS 🚇').classes('text-4xl font-bold text-white mb-4 text-center')
        
        # Game canvas container
        with ui.element('div').style('position: relative'):
            canvas = ui.canvas(width=settings.GAME_WIDTH, height=settings.GAME_HEIGHT).classes('game-canvas')
            
            # Game UI overlay
            with ui.element('div').classes('game-ui'):
                score_label = ui.label('Score: 0')
                coins_label = ui.label('Coins: 0')
                distance_label = ui.label('Distance: 0m')
            
            # Game over screen (initially hidden)
            with ui.element('div').classes('game-over-screen').style('display: none') as game_over_screen:
                ui.label('GAME OVER!').classes('text-3xl font-bold mb-4')
                final_score_label = ui.label('Final Score: 0')
                final_coins_label = ui.label('Coins Collected: 0')
                final_distance_label = ui.label('Distance: 0m')
                ui.button('RESTART', on_click=restart_game).classes('mt-4 bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-lg')
            
            # Controls info
            with ui.element('div').classes('controls-info'):
                ui.label('🎮 Controls:')
                ui.label('← → or A D: Move')
                ui.label('↑ or SPACE: Jump')
                ui.label('P: Pause')
    
    def restart_game():
        game.restart()
        game_over_screen.style('display: none')
    
    def draw_game(render_data):
        """Draw the game on canvas"""
        canvas.context.clearRect(0, 0, settings.GAME_WIDTH, settings.GAME_HEIGHT)
        
        # Draw background gradient
        gradient = canvas.context.createLinearGradient(0, 0, 0, settings.GAME_HEIGHT)
        gradient.addColorStop(0, '#87CEEB')
        gradient.addColorStop(0.7, '#98FB98')
        gradient.addColorStop(1, '#90EE90')
        canvas.context.fillStyle = gradient
        canvas.context.fillRect(0, 0, settings.GAME_WIDTH, settings.GAME_HEIGHT)
        
        # Draw background buildings
        for building in render_data['background']['buildings']:
            canvas.context.fillStyle = building['color']
            canvas.context.fillRect(building['x'], building['y'], building['width'], building['height'])
        
        # Draw clouds
        canvas.context.fillStyle = '#FFFFFF'
        for cloud in render_data['background']['clouds']:
            canvas.context.beginPath()
            canvas.context.arc(cloud['x'], cloud['y'], cloud['size'], 0, 2 * 3.14159)
            canvas.context.fill()
        
        # Draw ground
        canvas.context.fillStyle = settings.GROUND_COLOR
        ground_y = settings.GAME_HEIGHT - 100
        canvas.context.fillRect(0, ground_y, settings.GAME_WIDTH, 100)
        
        # Draw ground pattern
        canvas.context.fillStyle = '#A0522D'
        offset = render_data['background']['ground_offset']
        for i in range(-1, settings.GAME_WIDTH // 50 + 2):
            x = i * 50 - offset
            canvas.context.fillRect(x, ground_y + 10, 40, 5)
            canvas.context.fillRect(x + 10, ground_y + 20, 40, 5)
        
        # Draw obstacles
        canvas.context.fillStyle = settings.OBSTACLE_COLOR
        for obstacle in render_data['obstacles']:
            canvas.context.fillRect(obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height'])
            # Add some detail to obstacles
            canvas.context.fillStyle = '#1E5F8B'
            canvas.context.fillRect(obstacle['x'] + 5, obstacle['y'] + 5, obstacle['width'] - 10, 10)
            canvas.context.fillStyle = settings.OBSTACLE_COLOR
        
        # Draw coins
        canvas.context.fillStyle = settings.COIN_COLOR
        for coin in render_data['coins']:
            canvas.context.beginPath()
            canvas.context.arc(coin['x'] + coin['width']/2, coin['y'] + coin['height']/2, coin['width']/2, 0, 2 * 3.14159)
            canvas.context.fill()
            # Add coin shine effect
            canvas.context.fillStyle = '#FFFF99'
            canvas.context.beginPath()
            canvas.context.arc(coin['x'] + coin['width']/2 - 3, coin['y'] + coin['height']/2 - 3, 3, 0, 2 * 3.14159)
            canvas.context.fill()
            canvas.context.fillStyle = settings.COIN_COLOR
        
        # Draw player
        player = render_data['player']
        canvas.context.fillStyle = settings.PLAYER_COLOR
        canvas.context.fillRect(player['x'], player['y'], player['width'], player['height'])
        
        # Add player details (simple character)
        # Head
        canvas.context.fillStyle = '#FFB6C1'
        canvas.context.fillRect(player['x'] + 8, player['y'], 24, 20)
        
        # Eyes
        canvas.context.fillStyle = '#000000'
        canvas.context.fillRect(player['x'] + 12, player['y'] + 6, 4, 4)
        canvas.context.fillRect(player['x'] + 24, player['y'] + 6, 4, 4)
        
        # Body
        canvas.context.fillStyle = settings.PLAYER_COLOR
        canvas.context.fillRect(player['x'] + 5, player['y'] + 20, 30, 25)
        
        # Legs
        canvas.context.fillStyle = '#4169E1'
        canvas.context.fillRect(player['x'] + 8, player['y'] + 45, 10, 15)
        canvas.context.fillRect(player['x'] + 22, player['y'] + 45, 10, 15)
        
        canvas.update()
    
    # Keyboard event handlers
    def handle_key_down(e: events.KeyEventArguments):
        game.handle_input(e.key, True)
        if e.key == 'KeyP':  # Pause
            game.pause_toggle()
    
    def handle_key_up(e: events.KeyEventArguments):
        game.handle_input(e.key, False)
    
    # Set up keyboard listeners
    ui.keyboard(on_key=handle_key_down, events=['keydown'])
    ui.keyboard(on_key=handle_key_up, events=['keyup'])
    
    # Game loop
    async def game_loop():
        while True:
            render_data = game.update()
            
            # Update UI
            score_label.text = f'Score: {render_data["score"]}'
            coins_label.text = f'Coins: {render_data["coins_collected"]}'
            distance_label.text = f'Distance: {render_data["distance"]}m'
            
            # Draw game
            draw_game(render_data)
            
            # Show game over screen
            if render_data['game_over']:
                final_score_label.text = f'Final Score: {render_data["score"]}'
                final_coins_label.text = f'Coins Collected: {render_data["coins_collected"]}'
                final_distance_label.text = f'Distance: {render_data["distance"]}m'
                game_over_screen.style('display: block')
            
            await asyncio.sleep(1/settings.FPS)  # 60 FPS
    
    # Start game loop
    ui.timer(1/settings.FPS, game_loop)
    
    # Instructions
    with ui.card().classes('mt-4 bg-white/10 backdrop-blur-sm'):
        ui.label('🎯 How to Play:').classes('text-xl font-bold text-white mb-2')
        ui.label('• Avoid obstacles by moving left/right or jumping').classes('text-white')
        ui.label('• Collect golden coins for extra points').classes('text-white')
        ui.label('• The game gets faster as you progress!').classes('text-white')
        ui.label('• Try to beat your high score!').classes('text-white')