/**
 * takes half and half of each parents a and b to each of the children
 * 1111 0000
 * =
 * 1100 0011
 */
function integer_crossover(a:number,b:number):[number,number] {
    let c = (a & 0b1100) | (b & 0b0011)
    let d = (a & 0b0011) | (b & 0b1100)
    return [c,d];
}


export {integer_crossover}