/**
 * General structure for a multiobjective evolutionary optimization algorithm
 * ELEMENTTYPE is population element type
 * SCORETYPE is the return type of a objective function
 */
export class MOEA {
    /**
     * runs algorithm until continueIterating returns false
     */
    run() {
        let P = this.intializePopulation();
        let t = 0;
        while (this.continueIterating(P, t)) {
            this.onIterationStart(P, t);
            P = this.selection(P);
            P = this.variation(P);
            this.onIterationEnd(P, t);
            t++;
        }
    }
}
