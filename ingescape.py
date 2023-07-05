
import sys
import ingescape as igs

def multiply_callback(iop_type, iop_name, value_type, value, my_data):
    igs.info(f"From service, multiply {value} by 2 : {value * 2}")
    igs.output_set_int("out", value * 2)

#def multiply_service_callback(sender_agent_name, sender_agent_uuid, service_name, argument_list, token, my_data):
#    igs.info(f"From input, multiply {argument_list[0]} by {argument_list[1]} : {argument_list[0]*argument_list[1]}")
#    igs.service_call(sender_agent_uuid, "result", (argument_list[0]*argument_list[1]), "")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("usage: python3 ./main.py agent_name network_device port")
        list_devices = igs.net_devices_list()
        print("Use one of these devices :")
        for device in list_devices:
            print(f"    {device}")
        exit(1)

    igs.input_create("in2", igs.INTEGER_T, None)
    igs.observe_input("in2", multiply_callback, None)
    
    igs.mapping_add("in2", "multiply", "out")
    #igs_mapping_add("image", "ImagesProvider", "image")
    
    igs.output_create("out", igs.INTEGER_T, None)

    #igs.service_init("multiply", multiply_service_callback, None)
    #igs.service_arg_add("multiply", "a", igs.INTEGER_T)
    #igs.service_arg_add("multiply", "b", igs.INTEGER_T)

    igs.agent_set_name(sys.argv[1])
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    # simple main loop used to wait for user to stop the agent.
    input('')

    igs.stop()