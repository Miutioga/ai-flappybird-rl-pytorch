import pygame
from collections import deque
from copy import deepcopy

class BabyBirds:
    def __init__(self, num_babies=4, horizontal_spacing=8):
        self.num_babies = num_babies
        self.horizontal_spacing = horizontal_spacing
        # Store position history of the main bird for each baby
        self.position_history = deque(maxlen=num_babies * horizontal_spacing)
        # Store rotation history of the main bird
        self.rotation_history = deque(maxlen=num_babies * horizontal_spacing)
        # Store flap index history of the main bird
        self.flap_index_history = deque(maxlen=num_babies * horizontal_spacing)
        
    def update(self, player_x, player_y, player_rot, player_idx):
        """Update position history of the main bird"""
        self.position_history.append((player_x, player_y))
        self.rotation_history.append(player_rot)
        self.flap_index_history.append(player_idx)
        
    def get_baby_positions(self):
        """Get positions for all baby birds in horizontal formation"""
        baby_positions = []
        
        # Calculate positions for each baby bird
        for i in range(self.num_babies):
            history_index = (i + 1) * self.horizontal_spacing - 1
            if len(self.position_history) > history_index:
                # Get base position from history
                base_pos = self.position_history[-history_index]
                rot = self.rotation_history[-history_index]
                flap_idx = self.flap_index_history[-history_index]
                
                # Adjust x position to be more horizontal
                # Each baby bird is positioned behind the main bird with fixed horizontal spacing
                x = base_pos[0] - (i + 1) * self.horizontal_spacing
                y = base_pos[1]  # Keep same y as leader
                
                baby_positions.append({
                    'x': x,
                    'y': y,
                    'rot': rot,
                    'flap_idx': flap_idx
                })
                
        return baby_positions

    def check_crash(self, pipes, ground_y):
        """Check if any baby bird crashes with pipes or ground"""
        baby_positions = self.get_baby_positions()
        BIRD_WIDTH = 34 * 0.6  # Scaled width of baby birds (60% of original)
        BIRD_HEIGHT = 24 * 0.6  # Scaled height of baby birds (60% of original)
        
        for pos in baby_positions:
            # Check ground collision
            if pos['y'] + BIRD_HEIGHT >= ground_y - 1:
                return True
                
            # Check pipe collisions
            baby_rect = pygame.Rect(pos['x'], pos['y'], BIRD_WIDTH, BIRD_HEIGHT)
            
            for pipe in pipes:
                pipe_rect = pygame.Rect(
                    pipe['x'], 
                    pipe['y'], 
                    pipe['pipe_width'], 
                    pipe['pipe_height']
                )
                
                if baby_rect.colliderect(pipe_rect):
                    return True
                    
        return False

    def draw(self, surface, images):
        """Draw all baby birds"""
        baby_positions = self.get_baby_positions()
        
        # Scale factor for baby birds (make them smaller than the main bird)
        scale_factor = 0.6
        
        for pos in baby_positions:
            # Scale the bird image
            original_image = images['player'][pos['flap_idx']]
            scaled_size = (
                int(original_image.get_width() * scale_factor),
                int(original_image.get_height() * scale_factor)
            )
            scaled_image = pygame.transform.scale(original_image, scaled_size)
            
            # Rotate the scaled image
            rotated_image = pygame.transform.rotate(scaled_image, pos['rot'])
            
            # Get the rect for positioning
            image_rect = rotated_image.get_rect(
                center=(
                    pos['x'] + scaled_size[0] // 2,
                    pos['y'] + scaled_size[1] // 2
                )
            )
            
            # Draw the baby bird
            surface.blit(rotated_image, image_rect)