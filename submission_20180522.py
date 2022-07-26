from engine.const import Const
import util
import math
import random
import collections


############################################################
# Problem 1: Warmup
def get_conditional_prob1(delta, epsilon, eta, c2, d2):
    """
    :param delta: [δ] is the parameter governing the distribution of the initial car's position
    :param epsilon: [ε] is the parameter governing the conditional distribution of the next car's position given the previos car's position
    :param eta: [η] is the parameter governing the conditional distribution of the sensor's measurement given the current car's position
    :param c2: the car's 2nd position
    :param d2: the sensor's 2nd measurement

    :returns: a number between 0~1 corresponding to P(C_2=c2 | D_2=d2)
    """
    # Problem 1a
    # BEGIN_YOUR_ANSWER (our solution is 14 lines of code, but don't worry if you deviate from this)
    p_c2_zero = delta*(1-epsilon)+(1-delta)*epsilon
    p_c2_one = delta*epsilon+(1-delta)*(1-epsilon)

    p_c2_zero_d2_zero = (1-eta)*p_c2_zero
    p_c2_zero_d2_one = eta*p_c2_zero
    p_c2_one_d2_zero = eta*p_c2_one
    p_c2_one_d2_one = (1-eta)*p_c2_one

    if c2 == 0 and d2 == 0:
        return p_c2_zero_d2_zero/(p_c2_zero_d2_zero+p_c2_one_d2_zero)
    elif c2 == 0 and d2 == 1:
        return p_c2_zero_d2_one/(p_c2_zero_d2_one+p_c2_one_d2_one)
    elif c2 == 1 and d2 == 0:
        return p_c2_one_d2_zero/(p_c2_one_d2_zero+p_c2_zero_d2_zero)
    elif c2 == 1 and d2 == 1:
        return p_c2_one_d2_one/(p_c2_one_d2_one+p_c2_zero_d2_one)
    # END_YOUR_ANSWER


def get_conditional_prob2(delta, epsilon, eta, c2, d2, d3):
    """
    :param delta: [δ] is the parameter governing the distribution of the initial car's position
    :param epsilon: [ε] is the parameter governing the conditional distribution of the next car's position given the previos car's position
    :param eta: [η] is the parameter governing the conditional distribution of the sensor's measurement given the current car's position
    :param c2: the car's 2nd position
    :param d2: the sensor's 2nd measurement
    :param d3: the sensor's 3rd measurement

    :returns: a number between 0~1 corresponding to P(C_2=c2 | D_2=d2, D_3=d3)
    """
    # Problem 1b
    # BEGIN_YOUR_ANSWER (our solution is 17 lines of code, but don't worry if you deviate from this)
    p_c2_zero = delta*(1-epsilon)+(1-delta)*epsilon
    p_c2_one = delta*epsilon+(1-delta)*(1-epsilon)

    p_c2_zero_d2_zero_d3_zero = (1-eta)*p_c2_zero * \
        ((1-epsilon)*(1-eta)+epsilon*eta)
    p_c2_zero_d2_zero_d3_one = (1-eta)*p_c2_zero * \
        ((1-epsilon)*eta+epsilon*(1-eta))
    p_c2_zero_d2_one_d3_zero = eta*p_c2_zero*((1-epsilon)*(1-eta)+epsilon*eta)
    p_c2_zero_d2_one_d3_one = eta*p_c2_zero*((1-epsilon)*eta+epsilon*(1-eta))
    p_c2_one_d2_zero_d3_zero = eta*p_c2_one*(epsilon*(1-eta)+(1-epsilon)*eta)
    p_c2_one_d2_zero_d3_one = eta*p_c2_one*((1-epsilon)*(1-eta)+(epsilon)*eta)
    p_c2_one_d2_one_d3_zero = (1-eta)*p_c2_one * \
        (epsilon*(1-eta)+(1-epsilon)*eta)
    p_c2_one_d2_one_d3_one = (1-eta)*p_c2_one * \
        ((1-epsilon)*(1-eta)+(epsilon)*eta)

    if c2 == 0 and d2 == 0 and d3 == 0:
        return p_c2_zero_d2_zero_d3_zero/(p_c2_zero_d2_zero_d3_zero+p_c2_one_d2_zero_d3_zero)
    elif c2 == 0 and d2 == 0 and d3 == 1:
        return p_c2_zero_d2_zero_d3_one/(p_c2_zero_d2_zero_d3_one+p_c2_one_d2_zero_d3_one)
    elif c2 == 0 and d2 == 1 and d3 == 0:
        return p_c2_zero_d2_one_d3_zero/(p_c2_zero_d2_one_d3_zero+p_c2_one_d2_one_d3_zero)
    elif c2 == 0 and d2 == 1 and d3 == 1:
        return p_c2_zero_d2_one_d3_one/(p_c2_zero_d2_one_d3_one+p_c2_one_d2_one_d3_one)
    elif c2 == 1 and d2 == 0 and d3 == 0:
        return p_c2_one_d2_zero_d3_zero/(p_c2_one_d2_zero_d3_zero+p_c2_zero_d2_zero_d3_zero)
    elif c2 == 1 and d2 == 0 and d3 == 1:
        return p_c2_one_d2_zero_d3_one/(p_c2_one_d2_zero_d3_one+p_c2_zero_d2_zero_d3_one)
    elif c2 == 1 and d2 == 1 and d3 == 0:
        return p_c2_one_d2_one_d3_zero/(p_c2_one_d2_one_d3_zero+p_c2_zero_d2_one_d3_zero)
    elif c2 == 1 and d2 == 1 and d3 == 1:
        return p_c2_one_d2_one_d3_one/(p_c2_one_d2_one_d3_one+p_c2_zero_d2_one_d3_one)
    # END_YOUR_ANSWER


# Problem 1c
def get_epsilon():
    """
    return a value of epsilon (ε)
    """
    # Problem 1c
    # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
    return 0.5
    # END_YOUR_ANSWER


# Class: ExactInference
# ---------------------
# Maintain and update a belief distribution over the probability of a car
# being in a tile using exact updates (correct, but slow times).
class ExactInference(object):

    # Function: Init
    # --------------
    # Constructer that initializes an ExactInference object which has
    # numRows x numCols number of tiles.
    def __init__(self, numRows, numCols):
        self.skipElapse = (
            False  # ONLY USED BY GRADER.PY in case problem 3 has not been completed
        )
        # util.Belief is a class (constructor) that represents the belief for a single
        # inference state of a single car (see util.py).
        self.belief = util.Belief(numRows, numCols)
        self.transProb = util.loadTransProb()

    ############################################################
    # Problem 2:
    # Function: Observe (update the probablities based on an observation)
    # -----------------
    # Takes |self.belief| and updates it based on the distance observation
    # $d_t$ and your position $a_t$.
    #
    # - agentX: x location of your car (not the one you are tracking)
    # - agentY: y location of your car (not the one you are tracking)
    # - observedDist: true distance plus a mean-zero Gaussian with standard
    #                 deviation Const.SONAR_STD
    #
    # Notes:
    # - Convert row and col indices into locations using util.rowToY and util.colToX.
    # - util.pdf: computes the probability density function for a Gaussian
    # - Don't forget to normalize self.belief!
    ############################################################

    def observe(self, agentX, agentY, observedDist):
        # BEGIN_YOUR_ANSWER (our solution is 9 lines of code, but don't worry if you deviate from this)
        for row in range(self.belief.getNumRows()):
            for col in range(self.belief.getNumCols()):
                currProb = self.belief.getProb(row, col)
                y = util.rowToY(row)
                x = util.colToX(col)
                dist = math.sqrt((agentX - x)**2 + (agentY - y)**2)
                emsProb = util.pdf(dist, Const.SONAR_STD, observedDist)
                self.belief.setProb(row, col, currProb * emsProb)
        self.belief.normalize()
        # END_YOUR_ANSWER

    ############################################################
    # Problem 3:
    # Function: Elapse Time (propose a new belief distribution based on a learned transition model)
    # ---------------------
    # Takes |self.belief| and updates it based on the passing of one time step.
    # Notes:
    # - Use the transition probabilities in self.transProb, which gives all
    #   ((oldTile, newTile), transProb) key-val pairs that you must consider.
    # - Other ((oldTile, newTile), transProb) pairs not in self.transProb have
    #   zero probabilities and do not need to be considered.
    # - util.Belief is a class (constructor) that represents the belief for a single
    #   inference state of a single car (see util.py).
    # - Be sure to update beliefs in self.belief ONLY based on the current self.belief distribution.
    #   Do NOT invoke any other updated belief values while modifying self.belief.
    # - Use addProb and getProb to manipulate beliefs to add/get probabilities from a belief (see util.py).
    # - Don't forget to normalize self.belief!
    ############################################################
    def elapseTime(self):
        if self.skipElapse:
            return  # ONLY FOR THE GRADER TO USE IN Problem 2
        # BEGIN_YOUR_ANSWER (our solution is 8 lines of code, but don't worry if you deviate from this)
        nBelief = util.Belief(self.belief.getNumRows(),
                              self.belief.getNumCols(), 0)
        for transProbObject in self.transProb:
            (oldTile, newTile) = transProbObject
            nBelief.addProb(
                newTile[0], newTile[1], self.belief.getProb(oldTile[0], oldTile[1]) * self.transProb[transProbObject])
        nBelief.normalize()
        self.belief = nBelief
        # END_YOUR_ANSWER

    # Function: Get Belief
    # ---------------------
    # Returns your belief of the probability that the car is in each tile. Your
    # belief probabilities should sum to 1.

    def getBelief(self):
        return self.belief


# Class: Particle Filter
# ----------------------
# Maintain and update a belief distribution over the probability of a car
# being in a tile using a set of particles.
class ParticleFilter(object):

    NUM_PARTICLES = 200

    # Function: Init
    # --------------
    # Constructer that initializes an ParticleFilter object which has
    # numRows x numCols number of tiles.
    def __init__(self, numRows, numCols):
        self.belief = util.Belief(numRows, numCols)

        # Load the transition probabilities and store them in a dict of defaultdict
        # self.transProbDict[oldTile][newTile] = probability of transitioning from oldTile to newTile
        self.transProb = util.loadTransProb()
        self.transProbDict = dict()
        for (oldTile, newTile) in self.transProb:
            if not oldTile in self.transProbDict:
                self.transProbDict[oldTile] = collections.defaultdict(int)
            self.transProbDict[oldTile][newTile] = self.transProb[(
                oldTile, newTile)]

        # Initialize the particles randomly
        self.particles = collections.defaultdict(int)
        potentialParticles = list(self.transProbDict.keys())
        for i in range(self.NUM_PARTICLES):
            particleIndex = int(random.random() * len(potentialParticles))
            self.particles[potentialParticles[particleIndex]] += 1

        self.updateBelief()

    # Function: Update Belief
    # ---------------------
    # Updates |self.belief| with the probability that the car is in each tile
    # based on |self.particles|, which is a defaultdict from particle to
    # probability (which should sum to 1).
    def updateBelief(self):
        newBelief = util.Belief(self.belief.getNumRows(),
                                self.belief.getNumCols(), 0)
        for tile in self.particles:
            newBelief.setProb(tile[0], tile[1], self.particles[tile])
        newBelief.normalize()
        self.belief = newBelief

    ############################################################
    # Problem 4 (part a):
    # Function: Observe:
    # -----------------
    # Takes |self.particles| and updates them based on the distance observation
    # $d_t$ and your position $a_t$.
    # This algorithm takes two steps:
    # 1. Reweight the particles based on the observation.
    #    Concept: We had an old distribution of particles, we want to update these
    #             these particle distributions with the given observed distance by
    #             the emission probability.
    #             Think of the particle distribution as the unnormalized posterior
    #             probability where many tiles would have 0 probability.
    #             Tiles with 0 probabilities (no particles), we do not need to update.
    #             This makes particle filtering runtime to be O(|particles|).
    #             In comparison, exact inference (problem 2 + 3), most tiles would
    #             would have non-zero probabilities (though can be very small).
    # 2. Resample the particles.
    #    Concept: Now we have the reweighted (unnormalized) distribution, we can now
    #             resample the particles and update where each particle should be at.
    #
    # - agentX: x location of your car (not the one you are tracking)
    # - agentY: y location of your car (not the one you are tracking)
    # - observedDist: true distance plus a mean-zero Gaussian with standard deviation Const.SONAR_STD
    #
    # Notes:
    # - Create |self.NUM_PARTICLES| new particles during resampling.
    # - To pass the grader, you must call util.weightedRandomChoice() once per new particle.
    ############################################################
    def observe(self, agentX, agentY, observedDist):
        # BEGIN_YOUR_ANSWER (our solution is 12 lines of code, but don't worry if you deviate from this)
        particles = collections.defaultdict(float)
        for particle in self.particles:
            (row, col) = particle
            x = util.colToX(col)
            y = util.rowToY(row)
            dist = math.sqrt((agentX-x)**2+(agentY-y)**2)
            emsProb = util.pdf(dist, Const.SONAR_STD, observedDist)
            particles[(row, col)] = self.particles[particle] * emsProb
        nParticles = collections.defaultdict(int)
        for i in range(self.NUM_PARTICLES):
            particle = util.weightedRandomChoice(particles)
            nParticles[particle] += 1
        self.particles = nParticles
        # END_YOUR_ANSWER
        self.updateBelief()

    ############################################################
    # Problem 4 (part b):
    # Function: Elapse Time (propose a new belief distribution based on a learned transition model)
    # ---------------------
    # Read |self.particles| (defaultdict) corresonding to time $t$ and writes
    # |self.particles| corresponding to time $t+1$.
    # This algorithm takes one step
    # 1. Proposal based on the particle distribution at current time $t$:
    #    Concept: We have particle distribution at current time $t$, we want to
    #             propose the particle distribution at time $t+1$. We would like
    #             to sample again to see where each particle would end up using
    #             the transition model.
    #
    # Notes:
    # - transition probabilities is now using |self.transProbDict|
    # - Use util.weightedRandomChoice() to sample a new particle.
    # - To pass the grader, you must loop over the particles using
    #       for tile in self.particles
    #   and call util.weightedRandomChoice() $once per particle$ on the tile.
    ############################################################
    def elapseTime(self):
        # BEGIN_YOUR_ANSWER (our solution is 7 lines of code, but don't worry if you deviate from this)
        nParticles = collections.defaultdict(int)
        for particle in self.particles:
            for i in range(self.particles[particle]):
                nextParticle = util.weightedRandomChoice(
                    self.transProbDict[particle])

                if nextParticle in nParticles:
                    nParticles[nextParticle] += 1
                else:
                    nParticles[nextParticle] = 1

        self.particles = nParticles
        # END_YOUR_ANSWER

    # Function: Get Belief
    # ---------------------
    # Returns your belief of the probability that the car is in each tile. Your
    # belief probabilities should sum to 1.
    def getBelief(self):
        return self.belief
