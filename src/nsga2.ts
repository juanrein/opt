import { MOEA } from "./MOEA";


export class NSGA2<ELEMENTTYPE, SCORETYPE> extends MOEA<ELEMENTTYPE, SCORETYPE> {
    selection(P: ELEMENTTYPE[]): ELEMENTTYPE[] {
        throw new Error("Method not implemented.");
    }
    crossover(P: ELEMENTTYPE[]): ELEMENTTYPE[] {
        throw new Error("Method not implemented.");
    }
    mutation(P: ELEMENTTYPE[]): ELEMENTTYPE[] {
        throw new Error("Method not implemented.");
    }
    variation(P: ELEMENTTYPE[]): ELEMENTTYPE[] {
        throw new Error("Method not implemented.");
    }
    evaluateFitness(P: ELEMENTTYPE[]): [ELEMENTTYPE, SCORETYPE][] {
        throw new Error("Method not implemented.");
    }
    intializePopulation(): ELEMENTTYPE[] {
        throw new Error("Method not implemented.");
    }
    onIterationStart(P: ELEMENTTYPE[], t: number): void {
        throw new Error("Method not implemented.");
    }
    onIterationEnd(P: ELEMENTTYPE[], t: number): void {
        throw new Error("Method not implemented.");
    }
    continueIterating(P: ELEMENTTYPE[], t: number): boolean {
        throw new Error("Method not implemented.");
    }

}