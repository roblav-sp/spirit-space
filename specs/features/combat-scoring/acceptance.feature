Feature: Combat and scoring
  The player fires bullets that destroy enemies and score points.

  Scenario: Cooldown limits fire rate (AC-009)
    Given the fire input is held
    When less than 0.2 seconds pass since the last shot
    Then no additional bullet is created

  Scenario: Bullet destroys enemy and scores (AC-010)
    Given an enemy positioned directly above the player
    When a bullet reaches the enemy's bounding circle
    Then both bullet and enemy are removed
    And the score increases by 10

  Scenario: Miss does not score (AC-012)
    Given an enemy not on the bullet's path
    When the bullet passes it and leaves the top edge
    Then the score is unchanged and the bullet no longer exists
