Feature: Game over and restart
  Lethal events end the run; R starts a fresh one.

  Scenario: Enemy reaches the bottom (AC-013)
    Given an enemy whose bottom edge is at the world bottom
    When the simulation advances one frame
    Then GameOver is true

  Scenario: Enemy touches the player (AC-014)
    Given an enemy overlapping the player's bounding circle
    When the simulation advances one frame
    Then GameOver is true

  Scenario: Simulation freezes after game over (AC-015)
    Given GameOver is true
    When the simulation advances 1 second
    Then score, bullets, and enemies are unchanged

  Scenario: Restart resets everything (AC-016)
    Given GameOver is true with score 55
    When the player presses R
    Then the score is 0
    And no enemies or bullets exist
    And the player is centered near the bottom
    And GameOver is false
