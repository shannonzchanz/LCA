import numpy as np

class emission_models(object):

    def __init__(self, plastic_ef, cutleries_ef, container_ef, household, people_per_household, dishwashing_ef,
                 transport_ef,
                 transport_dist):
        self.packaging_subt = (plastic_ef + cutleries_ef + container_ef) * household * people_per_household

        self.transport_subt = transport_ef * transport_dist

        self.dishwashing_subt = dishwashing_ef * household * people_per_household

        self.total_emission = self.packaging_subt + self.transport_subt + self.dishwashing_subt


# packaging EF
plastic = {"yes": 0.1348, "no": 0}
cutleries = {"yes": 0.027535726, "no": 0}
container = {"yes": 0.086668372, "no": 0}

# transport EF
transport = {"gasoline car": 0.139, "electric car": 0.0739,
             "gasoline motorcycle": 0.06856236, "electric motorcycle": 0.004426,
             "gasoline bus": 0.019, "electric bus": 0.0068}

# dishwashing EF
water_ef = 0.001971588
soap_ef = 0.636421588
electricity_ef = 0.47844
water_ad = 0.9375
soap_ad = 0.00075
electricity_ad = 0.01875
dishwashing = {"yes": water_ef * water_ad + soap_ef * soap_ad + electricity_ef * electricity_ad, "no": 0}


def analysis(people_per_HH, dist_per_HH, HH, inter_cluster_dist):

    # analysis
    matrix = np.zeros((7, 6),) # matrix initialization

    for no_of_HH in range(1, HH+1):
        # as no of HH increases, total household distance increases
        total_household_dist = dist_per_HH * no_of_HH * 2
        # as no of HH increases, delivery distance still remains the same

        total_delivery_dist = dist_per_HH * 2 + inter_cluster_dist
        fd_gmotor_plastic_disposablecutleries = emission_models(plastic["yes"], cutleries["yes"], container["yes"], no_of_HH,
                                                                people_per_HH, dishwashing["no"],
                                                                transport["gasoline motorcycle"], total_delivery_dist)

        fd_gmotor_noplastic_disposablecutleries = emission_models(plastic["no"], cutleries["yes"], container["yes"], no_of_HH,
                                                                  people_per_HH, dishwashing["no"],
                                                                  transport["gasoline motorcycle"], total_delivery_dist)

        fd_gmotor_plastic_nocutleries = emission_models(plastic["yes"], cutleries["no"], container["yes"], no_of_HH,
                                                        people_per_HH, dishwashing["no"],
                                                        transport["gasoline motorcycle"], total_delivery_dist)

        fd_emotor_noplastic_disposablecutleries = emission_models(plastic["no"], cutleries["yes"], container["yes"], no_of_HH,
                                                                  people_per_HH, dishwashing["no"],
                                                                  transport["electric motorcycle"], total_delivery_dist)

        d_gcar_nondisposablecutleries = emission_models(plastic["no"], cutleries["no"], container["no"], no_of_HH,
                                                        people_per_HH, dishwashing["yes"],
                                                        transport["gasoline car"], total_household_dist)

        d_ecar_nondisposablecutleries = emission_models(plastic["no"], cutleries["no"], container["no"], no_of_HH,
                                                        people_per_HH, dishwashing["yes"],
                                                        transport["electric car"], total_household_dist)

        d_gbus_nondisposablecutleries = emission_models(plastic["no"], cutleries["no"], container["no"], no_of_HH,
                                                        people_per_HH, dishwashing["yes"],
                                                        transport["gasoline bus"], total_household_dist * people_per_HH)

        matrix[0][no_of_HH-1] = fd_gmotor_plastic_disposablecutleries.total_emission
        matrix[1][no_of_HH-1] = fd_gmotor_noplastic_disposablecutleries.total_emission
        matrix[2][no_of_HH-1] = fd_gmotor_plastic_nocutleries.total_emission
        matrix[3][no_of_HH-1] = fd_emotor_noplastic_disposablecutleries.total_emission
        matrix[4][no_of_HH-1] = d_gcar_nondisposablecutleries.total_emission
        matrix[5][no_of_HH-1] = d_ecar_nondisposablecutleries.total_emission
        matrix[6][no_of_HH-1] = d_gbus_nondisposablecutleries.total_emission

    print (matrix)

# analysis(people_per_HH, dist_per_HH, HH, inter_cluster_dist)
# same cluster, 3km away
analysis(3, 3, 6, 0)
# same cluster, 10km away
analysis(3, 10, 6, 0)
# different cluster, 3km away, inter-cluster 1.5km
analysis(3, 3, 6, 1.5)
# different cluster, 3km away, inter-cluster 6km
analysis(3, 3, 6, 6)



