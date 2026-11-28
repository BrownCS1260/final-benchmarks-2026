(define (loop n acc)
  (if (= n 0)
      acc
      (let ((on true))
        (let ((five 5))
          (let ((three 3))
            (loop (sub1 n)
                  (if on
                      (if (= (+ (+ 1 2) (+ three 4))
                             (+ (+ five three) (- five three)))
                          (+ acc 1)
                          (+ acc five))
                      (+ acc 100))))))))

(print (loop 1000000 0))
