from math import sqrt

rating_dict = {"Bob": {"12 Years a Slave": 1, "Gravity": 2,
                      "Blue Jasmin": 3, "American Hustle": 4,
                      "The Great Gatsby": 5},
         
         "Alice":{"12 Years a Slave": 4, "Gravity": 4.25,
                      "Blue Jasmin": 4.5, "American Hustle": 4.75,
                      "The Great Gatsby": 5}
                 }

def pearson_corr(dict1, dict2):
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_xsq = 0
    sum_ysq = 0
    n = 0
    for key in dict1:
        if key in dict2:
            n += 1
            x = dict1[key]
            y = dict2[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_xsq += pow(x, 2)
            sum_ysq += pow(y, 2)
    #denominator
    denominator = sqrt(sum_xsq - pow(sum_x, 2) / n) * sqrt(sum_ysq - pow(sum_y, 2) / n)
    if denominator == 0:
        return 0
    else:
        return (sum_xy - (sum_x * sum_y) / n) / denominator

#pearson_corr(rating_dict['Bob'], rating_dict['Alice'])