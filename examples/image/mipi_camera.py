from v4l2py import Device

with Device.from_id(0) as cam:
    for i, frame in enumerate(cam):
       print(f"frame #{i}: {len(frame)} bytes")
       if i > 9:
           break
