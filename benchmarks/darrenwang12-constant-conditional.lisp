(define (loop n acc)
  (if (= n 0)
      acc
      (let ((on true))
        (let ((five 5))
          (let ((three 3))
            (let ((two 2))
              (loop (sub1 n)
                    (if on
                        (if (< three five)
                            (if (= (+ (+ 1 two) (+ three 4))
                                   (+ (+ five three) (- five three)))
                                (+ acc (+ 1 two))
                                (+ acc five))
                            (+ acc 50))
                        (+ acc 100)))))))))

(print (loop 1000000 0))