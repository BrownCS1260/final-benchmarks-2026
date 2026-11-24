(define (inner n acc)
  (if (zero? n)
      acc
      (let ((k (+ (- 20 5) (add1 (sub1 3)))))
        (let ((k (if (= k 18) (+ k 1) 0)))
          (let ((smaller (< k 20)))
            (inner (sub1 n) (if smaller (+ acc k) (- acc k))))))))

(define (outer m acc)
  (if (zero? m)
      acc
      (outer (sub1 m) (+ acc (inner 1000 (- 5 5))))))

(print (outer 2000 0))