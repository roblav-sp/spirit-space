Feature: Enemy spawning and movement
  Enemies appear at the top and drift down at constant speed.

  Scenario: First spawn after one spawn delay (AC-005, AC-006)
    Given a freshly started game
    When the simulation advances 0.6 seconds
    Then no enemy exists
    When the simulation advances a further 0.6 seconds
    Then exactly one enemy exists

  Scenario: Spawn X stays on-screen (AC-007)
    Given a freshly started game
    When the simulation runs for 30 simulated seconds
    Then every spawned enemy X was within [enemyRadius, Width-enemyRadius]

  Scenario: Constant downward drift (AC-008)
    Given an enemy at Y0
    When the simulation advances dt seconds
    Then the enemy Y equals Y0 + 120*dt
