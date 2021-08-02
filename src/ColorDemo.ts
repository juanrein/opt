import { MOEA } from "./MOEA";

export async function animateProgression(history: RGB[][]) {
    let canvas = document.getElementById("canvas") as HTMLCanvasElement;
    let ctx = canvas.getContext("2d") as CanvasRenderingContext2D;
    for (let P of history) {
        await new Promise(resolve => setTimeout(resolve, 500));  
        ctx.clearRect(0, 0, 600, 400);
        for (let i=0; i<P.length; i++) {
            let member = P[i]
            let x = Math.floor(i / 6) * 100;
            let y = Math.floor(i % 6) * 100;
            let [r, g, b] = member;
            ctx.fillStyle = `rgb(${r},${g},${b})`
            ctx.fillRect(y, x, 100, 100);
        }
    }
}

type RGB = [number, number, number];
export class ColorProblem extends MOEA<RGB, [number,number]> {
    history: RGB[][];
    constructor() {
        super();
        this.history = [];
    }
    selection(P: RGB[]): RGB[] {
        let ef1f2 = this.evaluateFitness(P);
        ef1f2.sort((a, b) => {
            let [rgb1, [fa1,fa2]] = a;
            let [rgb2, [fb1,fb2]] = b;
            if (fa1 === fb1) {
                return fa2 - fb2;
            }
            return fa1 - fb1;
        })
        return ef1f2.slice(0, 12).map(e => e[0]);
    }
    crossover(P: RGB[]): RGB[] {
        let remaining = P.slice();
        let generated: RGB[] = [];
        while (generated.length < 24) {
            let i = Math.random() * remaining.length;
            let [p1] = remaining.splice(i, 1);
            i = Math.random() * remaining.length;
            let [p2] = remaining.splice(i, 1);
            let [r1, g1, b1] = p1
            let [r2, g2, b2] = p2
            generated.push(
                [r1 | r2, g1 | g2, b1 | b2],
                [r1 ^ r2, g1, b1 ^ b2],
                [r1 & r2, g1 & g2, b1 & b2],
                [r1 & r2, g1 | g2, b1 ^ b2],
            )
        }
        return generated;
    }
    mutation(P: RGB[]): RGB[] {
        let mutated: RGB[] = []
        for (let member of P) {
            let [r, g, b] = member;
            if (Math.random() < 1 / P.length) {
                r ^= 1 << Math.log2(r)
                g ^= 1 << Math.log2(g);
                b ^= 1 << Math.log2(b);
            }
            mutated.push([r, g, b])
        }
        return mutated;
    }
    variation(P: RGB[]): RGB[] {
        return this.mutation(this.crossover(P));
    }

    evaluateFitness(P: RGB[]): [RGB, [number,number]][] {
        let f1 = (e: RGB) => {
            let [r, g, b] = e;
            let [r1, g1, b1] = [160, 201, 44]
            return Math.sqrt((r - r1) ** 2 + (g - g1) ** 2 + (b - b1) ** 2);
        }
        let f2 = (e: RGB) => {
            let [r, g, b] = e;
            let [r1, g1, b1] = [103, 111, 138]
            return Math.sqrt((r - r1) ** 2 + (g - g1) ** 2 + (b - b1) ** 2);
        }

        return P.map((e: RGB) => [e, [f1(e), f2(e)]]);
    }
    intializePopulation(): RGB[] {
        function randomColor() {
            return Math.floor(Math.random() * 255);
        }
        
        function randomInit(): RGB {
            return [
                randomColor(),
                randomColor(),
                randomColor(),
            ]
        }
        let P: RGB[] = [];
        for (let i = 0; i < 24; i++) {
            let colors = randomInit();
            P.push(colors);
        }
        return P;
    }

    onIterationStart(P: RGB[], t: number) {
        this.history.push(P);
        
    }

    onIterationEnd(P: RGB[], t: number) {

    }
    continueIterating(P: RGB[], t: number): boolean {
        return t < 20;
    }

}
