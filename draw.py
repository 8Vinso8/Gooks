def optimised_draw(moved_gooks, bullets, bitmap, window):  # Bitmap заменить на название переменной карты
    # Закрашивание прошлых позиций
    for gook in moved_gooks:
        bitmap.draw_part(window, gook.get_last_pos(), gook.get_size())
    for bullet in bullets:
        bitmap.draw_part(window, bullet.get_last_pos(), bullet.get_size())
    # отрисовка объектов
    for gook in moved_gooks:
        gook.draw(window)
    for bullet in bullets:
        bullet.draw(window)
