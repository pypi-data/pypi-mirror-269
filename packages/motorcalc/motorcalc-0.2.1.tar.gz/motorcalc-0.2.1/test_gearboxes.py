import motorcalc.dcmotor as dcm
import motorcalc.dcmotorplot as dcplt
import motorcalc.dcmotorexport as dcexp

## generate a DC-Motor object
m=dcm.CDCMotor(U_N=3, I_0=0.030, k_M = 0.00194, R=11.1, application='C1021F', motor_name='DC-Motor')

## print its performance results
print(m)
# dcplt.CDCMotorPlot(m).plot_curves()
# dcexp.CDCMotorExport(dcm=m).list_spec_table()
# dcexp.CDCMotorExport(dcm=m, filename='text.xlsx').export_to_excel()
# dcexp.CDCMotorExport(dcm=m).export_to_excel('test2.xlsx')

# ## generate a gearbox-object
# gb = dcm.CGearbox(ratio=0.5,efficiency=0.8,name='test')

# ## add gearbox-object to gearboxes list
# m.add_gearbox(gb=gb)
# m.motor_name='DC Motor with gearbox-stage'
# ## print new performance results
# print(m)
# dcplt.CDCMotorPlot(m).plotCurves()


# ## add same gearbox-object to gearboxes list once again as a second stage
# m.add_gearbox(gb=gb)
# m.motor_name='DC Motor with two gearbox-stages'
# ## print new performance results
# print(m)
# dcplt.CDCMotorPlot(m).plotCurves()
