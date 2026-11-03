Feature: Player ship movement
  As a player I move my ship within the play field using keyboard input.

  Scenario: Move right at constant speed (AC-001)
    Given a freshly started game
    When the Right input is held for 1 simulated second at 60 FPS
    Then the player X equals Width/2 + 300, clamped to the field

  Scenario: Clamped at the left edge (AC-002)
    Given a freshly started game
    When the Left input is held for 10 simulated seconds
    Then the player X equals the player radius
    And the player remains within the play field

  Scenario: Frame-rate independence (AC-003, NFR-002)
    Given identical input sequences
    When the simulation runs 6 seconds at 30 FPS and at 60 FPS
    Then final player positions are identical within 1e-6

  Scenario: Corner clamping
    Given the player at the top-left corner
    When Left and Up inputs are held
    Then the player position does not change
