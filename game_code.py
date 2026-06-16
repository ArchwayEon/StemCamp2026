while running:
    clock.tick(60)          # cap at 60 frames/second

    for event in pygame.event.get():
        # Quit handler
        if event.type == pygame.QUIT:
            running = False
        # Restart handler
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                player.centerx = WIDTH // 2
                bullets.clear()
                asteroids.clear()
                score     = 0
                lives     = 3
                shoot_cooldown = 0
                spawn_timer    = 0
                game_over = False

    if not game_over:
        # ── Input ─────────────────────────────────────────
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]  and player.left  > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed
        if keys[pygame.K_SPACE] and shoot_cooldown == 0:
            bullet = pygame.Rect(player.centerx - 3,
                             player.top - 10, 6, 14)
            bullets.append(bullet)
            shoot_cooldown = 15     # wait 15 frames before next shot

        if shoot_cooldown > 0:
            shoot_cooldown -= 1

        # ── Move bullets ─────────────────────────────────
        for b in bullets[:]:
            b.y -= bullet_speed
            if b.bottom < 0:    # off the top of the screen
                bullets.remove(b)

        # ── Spawn asteroids ──────────────────────────────
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            size = random.randint(24, 48)
            x    = random.randint(size, WIDTH - size)
            asteroids.append(
                pygame.Rect(x - size, -size * 2,
                        size * 2,  size * 2))
            asteroid_speed = 3 + score // 5  # gets faster!

        # ── Move asteroids ───────────────────────────────
        for a in asteroids[:]:
            a.y += asteroid_speed
            if a.top > HEIGHT:
                asteroids.remove(a)

        # ── Collision: bullet hits asteroid ──────────────
        for b in bullets[:]:
            for a in asteroids[:]:
                if b.colliderect(a):
                    bullets.remove(b)
                    asteroids.remove(a)
                    score += 1
                    break

        # ── Collision: asteroid hits player ─────────────
        for a in asteroids[:]:
            if a.colliderect(player):
                asteroids.remove(a)
                lives -= 1
                if lives <= 0:
                    game_over = True

    screen.fill(BLACK)
    draw_stars()
    if not game_over:
        # ── Draw ship ────────────────────────────────────
        draw_ship(player)
        # ── Draw bullets ─────────────────────────────────
        for b in bullets:
            pygame.draw.rect(screen, YELLOW, b)
        # ── Draw asteroids ───────────────────────────────
        for a in asteroids:
            draw_asteroid(a)
        draw_hud()
    else:
        over_surf  = big_font.render("GAME OVER", True, RED)
        score_surf = font.render(f"Final Score: {score}", True, WHITE)
        restart    = font.render("Press R to play again", True, GRAY)
        screen.blit(over_surf,  (WIDTH//2 - over_surf.get_width()//2,  HEIGHT//2 - 80))
        screen.blit(score_surf, (WIDTH//2 - score_surf.get_width()//2, HEIGHT//2))
        screen.blit(restart,    (WIDTH//2 - restart.get_width()//2,    HEIGHT//2 + 50))

    pygame.display.flip()
