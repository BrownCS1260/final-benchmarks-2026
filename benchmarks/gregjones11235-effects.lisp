(define (noisy x) (do (print x) (newline) x))

(define (sum-c n acc)
  (if (zero? n)
      acc
      (sum-c (sub1 n) (+ acc (+ 5 (+ 2 (read-num)))))))

(define (spin n acc)
  (if (zero? n)
      acc
      (spin (sub1 n) (+ (+ acc 3) (+ 4 n)))))

(define (repeat k n acc)
  (if (zero? k) acc (repeat (sub1 k) n (+ acc (spin n 0)))))

(let ((a (read-num)))
  (let ((unused (noisy 42)))
    (let ((b (read-num)))
      (let ((c (if (< 1 0) (noisy 0) (- a b))))
        (do (print (sum-c 3 c))
            (newline)
            (print (repeat 1000 a 0))
            (newline))))))