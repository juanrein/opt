
/**
 * General structure for a multiobjective evolutionary optimization algorithm
 * ELEMENTTYPE is population element type
 * SCORETYPE is the return type of a objective function
 */
export abstract class MOEA<ELEMENTTYPE, SCORETYPE> {
    abstract selection(P: ELEMENTTYPE[]): ELEMENTTYPE[]; 
    abstract crossover(P: ELEMENTTYPE[]): ELEMENTTYPE[];
    abstract mutation(P: ELEMENTTYPE[]): ELEMENTTYPE[];
    abstract variation(P: ELEMENTTYPE[]): ELEMENTTYPE[];
    abstract evaluateFitness(P: ELEMENTTYPE[]): [ELEMENTTYPE, SCORETYPE][];
    abstract intializePopulation(): ELEMENTTYPE[];  
    /**
     * executed before every loop
     */
    abstract onIterationStart(P: ELEMENTTYPE[], t: number): void;
    /**
     * executed after every loop
     */
    abstract onIterationEnd(P: ELEMENTTYPE[], t: number): void;
    /**
     * end condition for the algorithm
     */
    abstract continueIterating(P: ELEMENTTYPE[], t: number): boolean

    /**
     * runs algorithm until continueIterating returns false
     */
    run() {
        let P = this.intializePopulation();
        let t = 0;
        while (this.continueIterating(P,t)) {
            this.onIterationStart(P, t);

            P = this.selection(P)
            P = this.variation(P);

            this.onIterationEnd(P, t);

            t++;
        }
    }
}
