import { MOEA } from "./MOEA";
export class NSGA2 extends MOEA {
    selection(P) {
        throw new Error("Method not implemented.");
    }
    crossover(P) {
        throw new Error("Method not implemented.");
    }
    mutation(P) {
        throw new Error("Method not implemented.");
    }
    variation(P) {
        throw new Error("Method not implemented.");
    }
    evaluateFitness(P) {
        throw new Error("Method not implemented.");
    }
    intializePopulation() {
        throw new Error("Method not implemented.");
    }
    onIterationStart(P, t) {
        throw new Error("Method not implemented.");
    }
    onIterationEnd(P, t) {
        throw new Error("Method not implemented.");
    }
    continueIterating(P, t) {
        throw new Error("Method not implemented.");
    }
}
