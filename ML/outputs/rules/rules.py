def findDecision(obj): #obj[0]: Gender, obj[1]: Customer Type, obj[2]: Age, obj[3]: Type of Travel, obj[4]: Class, obj[5]: Flight Distance, obj[6]: Inflight wifi service, obj[7]: Departure/Arrival time convenient, obj[8]: Ease of Online booking, obj[9]: Gate location, obj[10]: Food and drink, obj[11]: Online boarding, obj[12]: Seat comfort, obj[13]: Inflight entertainment, obj[14]: On-board service, obj[15]: Leg room service, obj[16]: Baggage handling, obj[17]: Checkin service, obj[18]: Inflight service, obj[19]: Cleanliness, obj[20]: Departure Delay in Minutes, obj[21]: Arrival Delay in Minutes
      else:
         return '1'
   else:
      return '0'
   # {"feature": "Online boarding", "instances": 82875, "metric_value": 0.9868, "depth": 1}
   if obj[11]<=3:
   # {"feature": "Online boarding", "instances": 82875, "metric_value": 0.9868, "depth": 1}
   if obj[11]<=3:
      # {"feature": "Inflight wifi service", "instances": 41811, "metric_value": 0.6073, "depth": 2}
      if obj[6]<=3:
      # {"feature": "Inflight wifi service", "instances": 41811, "metric_value": 0.6073, "depth": 2}
      if obj[6]<=3:
         # {"feature": "Ease of Online booking", "instances": 38031, "metric_value": 0.4672, "depth": 3}
         if obj[8]>0:
         # {"feature": "Ease of Online booking", "instances": 38031, "metric_value": 0.4672, "depth": 3}
         if obj[8]>0:
            # {"feature": "Class", "instances": 35776, "metric_value": 0.3641, "depth": 4}
            if obj[4]>0:
            # {"feature": "Class", "instances": 35776, "metric_value": 0.3641, "depth": 4}
            if obj[4]>0:
               # {"feature": "Type of Travel", "instances": 25574, "metric_value": 0.1313, "depth": 5}
               if obj[3]>0:
                  return '0'
               elif obj[3]<=0:
                  return '0'
               else:
                  return '0'
            elif obj[4]<=0:
               # {"feature": "Type of Travel", "instances": 25574, "metric_value": 0.1313, "depth": 5}
               if obj[3]>0:
                  return '0'
               elif obj[3]<=0:
                  return '0'
               else:
                  return '0'
            elif obj[4]<=0:
               # {"feature": "Inflight entertainment", "instances": 10202, "metric_value": 0.7181, "depth": 5}
               if obj[13]<=3:
                  return '0'
               elif obj[13]>3:
                  return '0'
               else:
                  return '0'
            else:
               return '0'
         elif obj[8]<=0:
               # {"feature": "Inflight entertainment", "instances": 10202, "metric_value": 0.7181, "depth": 5}
               if obj[13]<=3:
                  return '0'
               elif obj[13]>3:
                  return '0'
               else:
                  return '0'
            # {"feature": "Type of Travel", "instances": 2255, "metric_value": 0.9842, "depth": 4}
            if obj[3]<=0:
            else:
               return '0'
         elif obj[8]<=0:
               # {"feature": "Leg room service", "instances": 1172, "metric_value": 0.7787, "depth": 5}
               if obj[15]>0:
                  return '1'
               elif obj[15]<=0:
                  return '0'
               else:
                  return '1'
e of Travel", "instances": 2255, "metric_value": 0.9842, "depth": 4}
            if obj[3]<=0:
            elif obj[3]>0:
               # {"feature": "Leg room service", "instances": 1172, "metric_value": 0.7787, "depth": 5}
               if obj[15]>0:
                  return '1'
               # {"feature": "Flight Distance", "instances": 1083, "metric_value": 0.9443, "depth": 5}
               if obj[5]<=0:
                  return '0'
               else:
j[5]>0:
                  return '1'
               else:
                  return '0'
            else:
               return '1'
         else:
            return '0'
               # {"feature": "Flight Distance", "instances": 1083, "metric_value": 0.9443, "depth": 5}
               if obj[5]<=0:
                  return '0'
               elif obj[5]>0:
                  return '1'
               else:
                  return '0'
            else:
               return '1'
         else:
            return '0'
      elif obj[6]>3:
         # {"feature": "Leg room service", "instances": 3780, "metric_value": 0.9359, "depth": 3}
         if obj[15]<=4:
            # {"feature": "Gate location", "instances": 2718, "metric_value": 0.9923, "depth": 4}
         if obj[15]<=4:

               # {"feature": "Type of Travel", "instances": 1484, "metric_value": 0.8693, "depth": 5}
               if obj[3]<=0:
                  return '1'
            # {"feature": "Gate location", "instances": 2718, "metric_value": 0.9923, "depth": 4}
            if obj[9]>3:
0'
               else:
                  return '1'
            elif obj[9]<=3:
               # {"feature": "Type of Travel", "instances": 1484, "metric_value": 0.8693, "depth": 5}
               if obj[3]<=0:
                  return '1'
               elif obj[3]>0:
                  return '0'
               # {"feature": "Class", "instances": 1234, "metric_value": 0.9439, "depth": 5}
               if obj[4]>0:
                  return '0'
               else:
                  return '1'
               elif obj[4]<=0:
                  return '0'
            elif obj[9]<=3:
               else:
                  return '0'
            else:
               return '1'
         elif obj[15]>4:
               # {"feature": "Class", "instances": 1234, "metric_value": 0.9439, "depth": 5}
               if obj[4]>0:
                  return '0'
               elif obj[4]<=0:
                  return '0'
               else:
                  return '0'
            # {"feature": "Type of Travel", "instances": 1062, "metric_value": 0.4861, "depth": 4}
            if obj[3]<=0:
            else:
               return '1'
         elif obj[15]>4:
               # {"feature": "On-board service", "instances": 894, "metric_value": 0.2486, "depth": 5}
               if obj[14]>4:
                  return '1'
               elif obj[14]<=4:
                  return '1'
            # {"feature": "Type of Travel", "instances": 1062, "metric_value": 0.4861, "depth": 4}
            if obj[3]<=0:
               else:
                  return '1'
            elif obj[3]>0:
               # {"feature": "On-board service", "instances": 894, "metric_value": 0.2486, "depth": 5}
               if obj[14]>4:
                  return '1'
               # {"feature": "Ease of Online booking", "instances": 168, "metric_value": 0.9917, "depth": 5}
                  return '1'
                  return '0'
               else:
j[8]>4:
                  return '1'
               else:
]>0:
                  return '1'
            else:
               return '1'
         else:
            return '1'
re": "Ease of Online booking", "instances": 168, "metric_value": 0.9917, "depth": 5}
               if obj[8]<=4:
                  return '0'
      else:
  elif obj[8]>4:
                  return '1'
               else:
                  return '1'
   elif obj[11]>3:
            else:
               return '1'
         else:
            return '1'
      else:
         return '0'
   elif obj[11]>3:
      # {"feature": "Type of Travel", "instances": 41064, "metric_value": 0.8542, "depth": 2}
      if obj[3]<=0:
      # {"feature": "Type of Travel", "instances": 41064, "metric_value": 0.8542, "depth": 2}
      if obj[3]<=0:
         # {"feature": "Inflight entertainment", "instances": 32677, "metric_value": 0.6121, "depth": 3}
         if obj[13]>3:
         # {"feature": "Inflight entertainment", "instances": 32677, "metric_value": 0.6121, "depth": 3}
         if obj[13]>3:
            # {"feature": "Customer Type", "instances": 24647, "metric_value": 0.3831, "depth": 4}
            if obj[1]<=0:
            # {"feature": "Customer Type", "instances": 24647, "metric_value": 0.3831, "depth": 4}
            if obj[1]<=0:
               # {"feature": "Inflight wifi service", "instances": 22783, "metric_value": 0.2796, "depth": 5}
               if obj[6]>3:
                  return '1'
               elif obj[6]<=3:
                  return '1'
               else:
                  return '1'
            elif obj[1]>0:
               # {"feature": "Inflight wifi service", "instances": 22783, "metric_value": 0.2796, "depth": 5}
               if obj[6]>3:
                  return '1'
               elif obj[6]<=3:
                  return '1'
               else:
                  return '1'
            elif obj[1]>0:
               # {"feature": "Inflight wifi service", "instances": 1864, "metric_value": 0.9682, "depth": 5}
               if obj[6]<=4:
                  return '0'
               elif obj[6]>4:
                  return '1'
               else:
                  return '1'
            else:
               return '1'
               # {"feature": "Inflight wifi service", "instances": 1864, "metric_value": 0.9682, "depth": 5}
               if obj[6]<=4:
                  return '0'
         elif obj[13]<=3:
               elif obj[6]>4:
                  return '1'
               else:
                  return '1'
            else:
               return '1'
         elif obj[13]<=3:
            # {"feature": "Inflight wifi service", "instances": 8030, "metric_value": 0.9615, "depth": 4}
            if obj[6]<=4:
            # {"feature": "Inflight wifi service", "instances": 8030, "metric_value": 0.9615, "depth": 4}
            if obj[6]<=4:
               # {"feature": "Checkin service", "instances": 6694, "metric_value": 0.9957, "depth": 5}
               if obj[17]>2:
                  return '1'
               elif obj[17]<=2:
                  return '0'
               else:
                  return '1'
               # {"feature": "Checkin service", "instances": 6694, "metric_value": 0.9957, "depth": 5}
               if obj[17]>2:
                  return '1'
            elif obj[6]>4:
               elif obj[17]<=2:
                  return '0'
               else:
                  return '1'
            elif obj[6]>4:
               # {"feature": "Ease of Online booking", "instances": 1336, "metric_value": 0.0089, "depth": 5}
               if obj[8]>2:
                  return '1'
               elif obj[8]<=2:
                  return '1'
               else:
                  return '1'
Ease of Online booking", "instances": 1336, "metric_value": 0.0089, "depth": 5}
               if obj[8]>2:
                  return '1'
            else:
               elif obj[8]<=2:
                  return '1'
               else:
            return '1'
 '1'
            else:
               return '1'
         else:
            return '1'
      elif obj[3]>0:
         # {"feature": "Inflight wifi service", "instances": 8387, "metric_value": 0.7627, "depth": 3}
         if obj[6]<=4:
         # {"feature": "Inflight wifi service", "instances": 8387, "metric_value": 0.7627, "depth": 3}
         if obj[6]<=4:
            # {"feature": "Ease of Online booking", "instances": 7495, "metric_value": 0.554, "depth": 4}
            if obj[8]>3:
            # {"feature": "Ease of Online booking", "instances": 7495, "metric_value": 0.554, "depth": 4}
            if obj[8]>3:
               # {"feature": "Arrival Delay in Minutes", "instances": 3990, "metric_value": 0.7449, "depth": 5}
               if obj[21]>1:
                  return '0'
               elif obj[21]<=1:
                  return '0'
               else:
               # {"feature": "Arrival Delay in Minutes", "instances": 3990, "metric_value": 0.7449, "depth": 5}
               if obj[21]>1:
                  return '0'
            elif obj[8]<=3:
               elif obj[21]<=1:
                  return '0'
               else:
                  return '0'
            elif obj[8]<=3:
               # {"feature": "Leg room service", "instances": 3505, "metric_value": 0.2152, "depth": 5}
               if obj[15]>0:
                  return '0'
               elif obj[15]<=0:
                  return '0'
               else:
                  return '0'
               # {"feature": "Leg room service", "instances": 3505, "metric_value": 0.2152, "depth": 5}
               if obj[15]>0:
                  return '0'
            else:
               return '0'
<=0:
                  return '0'
               else:
:
                  return '0'
         else:
            else:
'0'
               return '0'
      else:
 obj[6]>4:
            return '1'
         else:
   else:
  return '0'
      return '0'
      else:
         return '1'
   else:
      return '0'
