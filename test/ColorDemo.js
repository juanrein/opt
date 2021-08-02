var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { MOEA } from "./MOEA";
export function animateProgression(history) {
    return __awaiter(this, void 0, void 0, function* () {
        let canvas = document.getElementById("canvas");
        let ctx = canvas.getContext("2d");
        for (let P of history) {
            yield new Promise(resolve => setTimeout(resolve, 500));
            ctx.clearRect(0, 0, 600, 400);
            for (let i = 0; i < P.length; i++) {
                let member = P[i];
                let x = Math.floor(i / 6) * 100;
                let y = Math.floor(i % 6) * 100;
                let [r, g, b] = member;
                ctx.fillStyle = `rgb(${r},${g},${b})`;
                ctx.fillRect(y, x, 100, 100);
            }
        }
    });
}
export class ColorProblem extends MOEA {
    constructor() {
        super();
        this.history = [];
    }
    selection(P) {
        let ef1f2 = this.evaluateFitness(P);
        ef1f2.sort((a, b) => {
            let [rgb1, [fa1, fa2]] = a;
            let [rgb2, [fb1, fb2]] = b;
            if (fa1 === fb1) {
                return fa2 - fb2;
            }
            return fa1 - fb1;
        });
        return ef1f2.slice(0, 12).map(e => e[0]);
    }
    crossover(P) {
        let remaining = P.slice();
        let generated = [];
        while (generated.length < 24) {
            let i = Math.random() * remaining.length;
            let [p1] = remaining.splice(i, 1);
            i = Math.random() * remaining.length;
            let [p2] = remaining.splice(i, 1);
            let [r1, g1, b1] = p1;
            let [r2, g2, b2] = p2;
            generated.push([r1 | r2, g1 | g2, b1 | b2], [r1 ^ r2, g1, b1 ^ b2], [r1 & r2, g1 & g2, b1 & b2], [r1 & r2, g1 | g2, b1 ^ b2]);
        }
        return generated;
    }
    mutation(P) {
        let mutated = [];
        for (let member of P) {
            let [r, g, b] = member;
            if (Math.random() < 1 / P.length) {
                r ^= 1 << Math.log2(r);
                g ^= 1 << Math.log2(g);
                b ^= 1 << Math.log2(b);
            }
            mutated.push([r, g, b]);
        }
        return mutated;
    }
    variation(P) {
        return this.mutation(this.crossover(P));
    }
    evaluateFitness(P) {
        let f1 = (e) => {
            let [r, g, b] = e;
            let [r1, g1, b1] = [160, 201, 44];
            return Math.sqrt(Math.pow((r - r1), 2) + Math.pow((g - g1), 2) + Math.pow((b - b1), 2));
        };
        let f2 = (e) => {
            let [r, g, b] = e;
            let [r1, g1, b1] = [103, 111, 138];
            return Math.sqrt(Math.pow((r - r1), 2) + Math.pow((g - g1), 2) + Math.pow((b - b1), 2));
        };
        return P.map((e) => [e, [f1(e), f2(e)]]);
    }
    intializePopulation() {
        function randomColor() {
            return Math.floor(Math.random() * 255);
        }
        function randomInit() {
            return [
                randomColor(),
                randomColor(),
                randomColor(),
            ];
        }
        let P = [];
        for (let i = 0; i < 24; i++) {
            let colors = randomInit();
            P.push(colors);
        }
        return P;
    }
    onIterationStart(P, t) {
        this.history.push(P);
    }
    onIterationEnd(P, t) {
    }
    continueIterating(P, t) {
        return t < 20;
    }
}
