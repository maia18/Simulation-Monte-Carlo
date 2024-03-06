# Simulation Monte Carlo - Cellular Wireless Communication Systems
import numpy as np ; import matplotlib.pyplot as plt ; from matplotlib.patches import Polygon ; from math import sqrt,log10,log2, pi, cos, sin, ceil

class PointAcess: # Point Acess

  channel = list(range(1,6)) # Channels

  # class constructor
  def __init__(self, coverage_area:tuple, power_=0):

    assert not isinstance(power_, (str, bool, list, tuple)) and ( power_ >= 0 ) # Power must be an number positive
    assert (type(coverage_area) == tuple) and ( len(coverage_area) >= 0 ) # Coverage area must be an tuple with len positive
    self.__coveragearea = (coverage_area) # Coverage Area of AP
    self.__power = power_ # Power of AP

  # Get coverage area
  @property
  def coverage_area(self):

    return self.__coveragearea

  # Set coverage area
  @coverage_area.setter
  def coverage_area(self, coverage_area_:tuple):

    assert type(coverage_area_) == tuple and ( len(coverage_area_) >= 0 ) # New Coverage area must be an tuple with len positive
    self.__coveragearea = (coverage_area_) # New Coverage Area


  # Get power
  @property
  def power(self):

    return self.__power

  # Set power
  @power.setter
  def power(self, power__):

    assert not isinstance(power__, (str, bool, list, tuple)) and ( power__ >= 0 ) # Power must be an number positive
    self.__power = power__ # New Power 


  def position_ap(self, position_:tuple): # Position - AP

    assert isinstance(position_, tuple) and ( len(position_) >= 0 ) # Position must be an tuple with len postive

    height, width = self.coverage_area

    if 0 <= position_[0] < height and 0 <= position_[1] < width:
        self.__position = position_
        self.__coveragearea[self.__position[0]:self.__position[0] + 10, self.__position[1]:self.__position[1] + 10] = 1
        return self.__position

    else:
        raise AssertionError("Position out of the coverage area...")



class UserEquipments: # User Equipments

  # class constructor
  def __init__(self, power_=1):

    assert not isinstance(power_, (str, bool, list, tuple)) and ( power_ >= 0 ) # Power must be an number positive
    self.__channel = np.random.choice(PointAcess.channel) # Choose an channel
    self.__power = power_ # Power of UE

  # Get power
  @property
  def power(self):

    return self.__power

  # Set power
  @power.setter
  def power(self, power__):

    assert not isinstance(power__, (str, bool, list, tuple)) and ( power__ >= 0 ) # Power must be an number positive
    self.__power = power__


  def position_ue(self, position_:tuple): # Position - UE

    assert isinstance(position_, tuple) and ( len(position_) >= 0 ) # Position must be an tuple with len postive
    self.__position = position_
    return self.__position


  # Get channel
  def get_channel(self):

    return self.__channel



class System: # System

  # class constructor
  def __init__(self):

    self.__aps = list()  # Point Acess
    self.__ues = list()  # User Equipments

  # Get AP's
  @property
  def aps(self):

    return self.__aps

  # Set AP's
  @aps.setter
  def aps(self, aps_: list[PointAcess]):

    assert isinstance(aps_, list) # AP must be an instance of the class PointAcess for be add on the list
    self.__aps.extend(aps_)


  # Get UE's
  @property
  def ues(self):

    return self.__ues

  # Set UE's
  @ues.setter
  def ues(self, ues: UserEquipments):

    assert isinstance(ues, UserEquipments) # UE must be an instance of the class UserEquipments for be add on the list
    self.__ues.append(ues)



class Simulation: # Simulation

  # class constructor
  def __init__(self, system:System):

    assert isinstance(system, System) # system must be an instance of the class System
    self.system = system
    self.coords = list() # Coordinates ocupeds

    self.bt = (10**(8)) # Total available bandwidth ( 100MHz = 10^(8)Hz )
    self.ko = (10**(-20)) # Constant for the noise power ( 10^(-17)miliwatts/Hz = 10^(-20)watts/Hz )
    self.do = 1 # fixed reference distance ( 1 meter )
    self.k = (10**(-4)) # Constant for the propagation model
    self.n = 4 # Constant for the propagation model

  def AP_position(self, aps: list[PointAcess]):
    
    assert len(aps) > 0 and isinstance(aps, list) # Amount of APs must be bigger than zero

    num_aps = len(aps)
    
    for i in range(num_aps):
        
        while True:

          x = ((i % int(sqrt(num_aps))) + 0.5) * 1000 / (int(sqrt(num_aps)))
          y = ((i // int(sqrt(num_aps))) + 0.5) * 1000 / ceil(num_aps / int(sqrt(num_aps)))

          if self.coords.__contains__((x, y)) == False:

            pos_ap = (x, y)

            aps[i].position_ap = pos_ap
            # self.ap_positions.append(aps[i].position_ap)
            self.coords.append(aps[i].position_ap)
            break

          
  def UE_position(self, ues: list[UserEquipments], aps: list[PointAcess]): # Position UE

    assert isinstance(ues, list) and isinstance(aps, list) # ues and aps must be an list of the PointAcess

    num_ues = len(ues)
    ap = np.random.choice(aps)

    for i in range(num_ues):
      
      while True:

        x = np.random.randint(0, 1000) 
        y = np.random.randint(0, 1000)
        distance_ue_ap = sqrt( ( ( ( x - ap.position_ap[0] ) ** 2 ) ) + ( ( ( y - ap.position_ap[1] ) ** 2 ) ) )

        if (self.coords.__contains__((x, y)) == False) and (distance_ue_ap >= self.do):

          pos_ue = (x, y)
          ues[i].position_ue = pos_ue
          self.coords.append(ues[i].position_ue)
          break



if __name__ == "__main__":

  sirs = [] # sirs totallys
  sinrs = [] # sinrs totallys
  capacities = [] # capacities totallys

  num_sim = 10 # Amount of simulations

  system = System()
  simulate = Simulation(system)

  num_ap = 64
  aps_ = [PointAcess((1000, 1000), 10) for _ in range(num_ap)]

  system.aps = aps_
    
  simulate.AP_position(aps_)

  for i, ap in enumerate(system.aps):
    print(f"AP {i+1} - Position: {ap.position_ap}")

  noise_power = ( ( simulate.ko ) * ( simulate.bt / len( ap.channel ) ) if len( ap.channel ) >= 0 else None ) # Noise power
  print(f'Noise Power: {noise_power}W \n')

  num_ue = 10 # Amount of UEs
  ues_ = [UserEquipments() for _ in range(num_ue)]

  for ue in ues_:

    system.ues = ue

  for _ in range(num_sim):
    
    simulate.UE_position(ues_, aps_)

    for i, ue in enumerate(ues_):
      print(f"Position UE{i+1}: {ue.position_ue}") # Position UE
      print(f"UE{i+1} Channel: {ue.get_channel()}") # Channel UE

      for j, ap in enumerate(aps_):

        distances_ue_ap_min = [sqrt((ue.position_ue[0] - ap.position_ap[0]) ** 2 + (ue.position_ue[1] - ap.position_ap[1]) ** 2) for ap in aps_]
        distance_ue_ap = sqrt((ue.position_ue[0] - ap.position_ap[0]) ** 2 + (ue.position_ue[1] - ap.position_ap[1]) ** 2)

        if distance_ue_ap == min(distances_ue_ap_min):
            print(f"Distance UE{i+1}-AP{j+1}: {distance_ue_ap}m") # Distance AP-UE
            power = ( ue.power * ( simulate.k / ( distance_ue_ap ** ( simulate.n ) ) ) ) # Power in Watts
            print(f"Power UE{i+1}-AP{j+1}: {power}W")

        interference_ = 0

        for k_, others_ues in enumerate(ues_):
        
          if ( ( others_ues.get_channel() == ue.get_channel() ) and ( others_ues != ue ) ):
          
            distance_othersUes_ap = sqrt( ( ( ( others_ues.position_ue[0] - ap.position_ap[0] ) ** (2) ) + ( ( others_ues.position_ue[1] - ap.position_ap[1] ) ** (2) ) ) )
            interference_ += ((( others_ues.power * ( simulate.k / ( distance_othersUes_ap ** ( simulate.n ) ) ) ))) # interference totally

        if interference_ > 0:

          sir = ( ( power / interference_ ) ) # SIR in Watts
          sinr = ( ( power / ( interference_ + noise_power ) ) ) # SINR in Watts
          capacity = ( ( simulate.bt / len(ap.channel) ) * ( log2(1 + sinr) ) ) # Capacity in bps
          
          print("- "*80) ; print(f"Signal-to-interference ratio(SIR): {sir}W") ; sirs.append(sir)
          print(f"Signal-to-interference-Noise ratio(SINR): {sinr}W") ; sinrs.append(sinr)
          print(f"Capacity: {capacity}bps") ; capacities.append(capacity) ; print("- "*80) ; print("\n")
    
          sir_db = [10 * log10(sir_) for sir_ in sirs]
          sinr_db = [10 * log10(sinr_) for sinr_ in sinrs]
          capacity_db = [(capacitie_) for capacitie_ in capacities]

  fig, axs = plt.subplots(2, 2, figsize=(12, 10)) # Graphic

  for ap in system.aps:

    points = [(ap.position_ap[0],ap.position_ap[1] + 20), (ap.position_ap[0] - 20, ap.position_ap[1] - 20), (ap.position_ap[0] + 20, ap.position_ap[1] - 20)]
    triangle = Polygon(points, closed=True, edgecolor='red', facecolor='red')
    axs[0, 0].add_patch(triangle)
    axs[0, 0].set_title("Simulate")

    for ue in system.ues:

      axs[0, 0].scatter(ue.position_ue[0], ue.position_ue[1], color='black', marker='.')
      axs[0, 0].set_xlim(0, 1000)
      axs[0, 0].set_ylim(0, 1000)

    for result, label, row, col in zip([sir_db, sinr_db, capacity_db], ['SIR', 'SINR', 'Capacity'], [0, 1, 1], [1, 0, 1]):

      filtered_result = [value for value in result if value is not None]
      filtered_result.sort()
      cumulative_prob = np.linspace(0, 1, len(filtered_result))
      axs[row, col].plot(filtered_result, cumulative_prob, label=f"CDF - {label}")
      axs[row, col].set_title(f"CDF - {label}")
      axs[row, col].grid(True)

  plt.show()
