import unittest

from Animations import AnimationStateMachine

class testAnim:
    def __init__(self):
        self.animationPath = "test/path"
    def tickAnim(self, animationFrame):
        pass


class MyTestCase(unittest.TestCase):

    def setup(self):
        machine = AnimationStateMachine(0, testAnim())
        idlestate = AnimationStateMachine.AnimationState("images/Player/Idle/", 60, "Idle")
        runningstate = AnimationStateMachine.AnimationState("images/Player/running/", 60, "running")
        jumpstate = AnimationStateMachine.AnimationState("images/Player/jump/", 40, "jump")
        landstate = AnimationStateMachine.AnimationState("images/Player/land/", 40, "land")

        idleToRunning = AnimationStateMachine.AnimationEdge(0, 1, "StartRunning")
        idleToJumping = AnimationStateMachine.AnimationEdge(0, 2, "Jumping")
        runningToJumping = AnimationStateMachine.AnimationEdge(1, 2, "Jumping")
        runningToIdle = AnimationStateMachine.AnimationEdge(1, 0, "StopRunning", [[1, False]])
        jumpingToLanding = AnimationStateMachine.AnimationEdge(2, 3, None)
        landingToIdle = AnimationStateMachine.AnimationEdge(3, 0, None)
        landingToRunning = AnimationStateMachine.AnimationEdge(3, 1, None, [[1, True]])

        machine.addState(idlestate)
        machine.addState(runningstate)
        machine.addState(jumpstate)
        machine.addState(landstate)

        machine.addEdge(idleToRunning)
        machine.addEdge(idleToJumping)
        machine.addEdge(runningToJumping)
        machine.addEdge(runningToIdle)
        machine.addEdge(jumpingToLanding)
        machine.addEdge(landingToIdle)
        machine.addEdge(landingToRunning)
        machine.setup()

        return machine

    def setup2(self):
        machine = AnimationStateMachine(0, testAnim())
        idlestate = AnimationStateMachine.AnimationState("images/Player/Idle/", 10, "Idle")
        runningstate = AnimationStateMachine.AnimationState("images/Player/running/", 10, "running")
        jumpstate = AnimationStateMachine.AnimationState("images/Player/jump/", 10, "jump")

        idleToRunning = AnimationStateMachine.AnimationEdge(0, 1, None)
        runningToJumping = AnimationStateMachine.AnimationEdge(1, 2, None)
        jumpingToIdle = AnimationStateMachine.AnimationEdge(2, 0, None)

        machine.addState(idlestate)
        machine.addState(runningstate)
        machine.addState(jumpstate)

        machine.addEdge(idleToRunning)
        machine.addEdge(runningToJumping)
        machine.addEdge(jumpingToIdle)
        machine.setup()

        return machine

    def test_null(self):
        machine = AnimationStateMachine(0, testAnim())
        with self.assertRaises(IndexError):
            machine.tick()

    def test_statenumber(self):
        testmachine = self.setup()
        self.assertEqual(len(testmachine.states), 4)

    def test_edgenumber(self):
        testmachine = self.setup()
        self.assertEqual(len(testmachine.edges), 7)

    def test_autopass(self):
        testmachine = self.setup2()
        for x in range(60):
            testmachine.tick()
        self.assertEqual(testmachine.state, 0)


if __name__ == '__main__':
    unittest.main()
