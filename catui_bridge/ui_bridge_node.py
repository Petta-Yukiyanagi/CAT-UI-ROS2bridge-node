#!/usr/bin/env python3
import json
import os
import rclpy
from rclpy.node import Node
from catui_bridge.msg import CatUICommand

class CatUIBridge(Node):
    def __init__(self):
        super().__init__('catui_bridge')

        self.declare_parameter(
            'ipc_root',
            '/opt/catui/CAT-UI-ROS2node/data/ipc'
        )
        self.ipc_root = self.get_parameter(
            'ipc_root'
        ).get_parameter_value().string_value

        os.makedirs(self.ipc_root, exist_ok=True)

        self.sub = self.create_subscription(
            CatUICommand,
            'catui/command',
            self.on_command,
            10
        )

        self.get_logger().info(
            f'CatUIBridge started. ipc_root={self.ipc_root}'
        )

    def on_command(self, msg: CatUICommand):
        tmp = os.path.join(self.ipc_root, 'ui_command.json.tmp')
        # broadcast ディレクトリを使う
        broadcast_dir = os.path.join(self.ipc_root, 'broadcast')
        os.makedirs(broadcast_dir, exist_ok=True)

        tmp = os.path.join(broadcast_dir, 'ui_command.json.tmp')
        dst = os.path.join(broadcast_dir, 'ui_command.json')

        data = {
            'face': int(msg.face_id),
            'text': msg.text,
            'reset_after': int(msg.reset_after)
        }

        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

        os.replace(tmp, dst)

def main():
    rclpy.init()
    node = CatUIBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
