import {ColorProblem, animateProgression} from "./ColorDemo"
import * as ops from "./operations"

function demo1() {
    let problem = new ColorProblem();

    problem.run();
    animateProgression(problem.history)
}
/* window.onload = () => {
    console.log(ops.integer_crossover(0b1111, 0b0000));
}
 */

console.log(ops.integer_crossover(0b1111, 0b0000));
