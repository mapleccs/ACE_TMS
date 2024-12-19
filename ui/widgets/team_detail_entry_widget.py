from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFormLayout, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView,
    QDateEdit, QSpinBox, QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QDate
import os
import datetime
from utils.logger import logger


class TeamDetailEntryWidget(QWidget):
    def __init__(self, team_service=None, parent=None):
        super().__init__(parent)
        self.team_service = team_service
        self.setup_ui()
        logger.debug("TeamDetailEntryWidget 初始化完成")

    def setup_ui(self):
        # 主布局
        main_layout = QVBoxLayout()

        # 表单布局
        form_layout = QFormLayout()

        # 队伍名称
        self.team_name_edit = QLineEdit()
        self.team_name_edit.setObjectName("team_name_edit")
        form_layout.addRow(QLabel("队伍名称:"), self.team_name_edit)

        # 队伍简称
        self.team_abbreviation_edit = QLineEdit()
        self.team_abbreviation_edit.setObjectName("team_abbreviation_edit")
        form_layout.addRow(QLabel("队伍简称:"), self.team_abbreviation_edit)

        # 队伍Logo
        logo_layout = QHBoxLayout()
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(100, 100)
        self.logo_label.setObjectName("logo_label")
        self.logo_label.setStyleSheet("border: 1px solid black;")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_path = None  # 存储Logo的路径
        logo_layout.addWidget(self.logo_label)

        self.select_logo_button = QPushButton("选择Logo")
        self.select_logo_button.setObjectName("select_logo_button")
        self.select_logo_button.clicked.connect(self.select_logo)
        logo_layout.addWidget(self.select_logo_button)

        form_layout.addRow(QLabel("队伍Logo:"), logo_layout)

        # 队长信息
        captain_layout = QHBoxLayout()
        self.captain_id_edit = QLineEdit()
        self.captain_id_edit.setObjectName("captain_id_edit")
        self.captain_qq_edit = QLineEdit()
        self.captain_qq_edit.setObjectName("captain_qq_edit")
        captain_form = QFormLayout()
        captain_form.addRow(QLabel("队长ID:"), self.captain_id_edit)
        captain_form.addRow(QLabel("队长QQ:"), self.captain_qq_edit)
        captain_layout.addLayout(captain_form)
        form_layout.addRow(QLabel("队长信息:"), captain_layout)

        # 联系方式1
        self.contact1_edit = QLineEdit()
        self.contact1_edit.setObjectName("contact1_edit")
        form_layout.addRow(QLabel("联系方式1:"), self.contact1_edit)

        # 联系方式2
        self.contact2_edit = QLineEdit()
        self.contact2_edit.setObjectName("contact2_edit")
        form_layout.addRow(QLabel("联系方式2:"), self.contact2_edit)

        # 队员信息
        member_layout = QVBoxLayout()
        member_header_layout = QHBoxLayout()
        member_header_layout.addWidget(QLabel("队员信息:"))

        self.add_member_button = QPushButton("添加队员")
        self.add_member_button.setObjectName("add_member_button")
        self.add_member_button.clicked.connect(self.add_member)
        self.remove_member_button = QPushButton("移除选中队员")
        self.remove_member_button.setObjectName("remove_member_button")
        self.remove_member_button.clicked.connect(self.remove_selected_member)
        member_header_layout.addWidget(self.add_member_button)
        member_header_layout.addWidget(self.remove_member_button)

        member_layout.addLayout(member_header_layout)

        self.members_table = QTableWidget(0, 6)
        self.members_table.setObjectName("members_table")
        self.members_table.setHorizontalHeaderLabels([
            "比赛昵称", "常用位置", "游戏ID", "个人积分", "QQ号", "队内职务"
        ])
        self.members_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.members_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        member_layout.addWidget(self.members_table)

        form_layout.addRow(member_layout)

        # 成立日期
        self.create_date_edit = QDateEdit()
        self.create_date_edit.setObjectName("create_date_edit")
        self.create_date_edit.setCalendarPopup(True)
        self.create_date_edit.setDate(QDate.currentDate())
        form_layout.addRow(QLabel("成立日期:"), self.create_date_edit)

        # 队伍积分
        self.team_points_spin = QSpinBox()
        self.team_points_spin.setObjectName("team_points_spin")
        self.team_points_spin.setRange(0, 1000000)
        form_layout.addRow(QLabel("队伍积分:"), self.team_points_spin)

        # 添加表单布局到主布局
        main_layout.addLayout(form_layout)

        # 保存按钮
        save_button = QPushButton("保存")
        save_button.setObjectName("save_button")
        save_button.clicked.connect(self.save_details)
        main_layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(main_layout)

    def select_logo(self):
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择队伍Logo", "", "Image Files (*.png *.jpg *.bmp)", options=options
        )
        if file_path:
            self.logo_path = file_path
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap.scaled(
                    self.logo_label.size(), Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ))
                logger.debug(f"选择Logo: {file_path}")
            else:
                QMessageBox.warning(self, "错误", "无法加载选择的图片。")
                logger.error(f"无法加载Logo图片: {file_path}")

    def add_member(self):
        row_position = self.members_table.rowCount()
        self.members_table.insertRow(row_position)
        logger.debug("添加新队员行")

    def remove_selected_member(self):
        selected_rows = self.members_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "移除队员", "请先选择要移除的队员。")
            logger.warning("尝试移除队员但未选择任何行")
            return
        for selected_row in reversed(selected_rows):
            self.members_table.removeRow(selected_row.row())
            logger.debug(f"移除队员行: {selected_row.row()}")

    def save_details(self):
        # 收集所有数据
        team_name = self.team_name_edit.text().strip()
        team_abbreviation = self.team_abbreviation_edit.text().strip()
        logo_path = self.logo_path  # 需要保存或上传
        captain_id = self.captain_id_edit.text().strip()
        captain_qq = self.captain_qq_edit.text().strip()
        contact1 = self.contact1_edit.text().strip()
        contact2 = self.contact2_edit.text().strip()
        create_date = self.create_date_edit.date().toPyDate()
        team_points = self.team_points_spin.value()

        # 收集队员信息
        members = []
        for row in range(self.members_table.rowCount()):
            member = {
                'nickname': self.members_table.item(row, 0).text().strip() if self.members_table.item(row, 0) else '',
                'position': self.members_table.item(row, 1).text().strip() if self.members_table.item(row, 1) else '',
                'game_id': self.members_table.item(row, 2).text().strip() if self.members_table.item(row, 2) else '',
                'individual_points': self.members_table.item(row, 3).text().strip() if self.members_table.item(row,
                                                                                                               3) else '',
                'qq_number': self.members_table.item(row, 4).text().strip() if self.members_table.item(row, 4) else '',
                'role': self.members_table.item(row, 5).text().strip() if self.members_table.item(row, 5) else '',
            }
            members.append(member)

        # 验证必填字段
        if not team_name:
            QMessageBox.warning(self, "验证错误", "队伍名称不能为空。")
            logger.warning("保存队伍信息失败: 队伍名称为空")
            return
        if not team_abbreviation:
            QMessageBox.warning(self, "验证错误", "队伍简称不能为空。")
            logger.warning("保存队伍信息失败: 队伍简称为空")
            return
        if not captain_id:
            QMessageBox.warning(self, "验证错误", "队长ID不能为空。")
            logger.warning("保存队伍信息失败: 队长ID为空")
            return
        if not captain_qq:
            QMessageBox.warning(self, "验证错误", "队长QQ不能为空。")
            logger.warning("保存队伍信息失败: 队长QQ为空")
            return

        # 构建团队数据字典
        team_data = {
            'team_name': team_name,
            'team_abbreviation': team_abbreviation,
            'team_logo': logo_path,
            'captain_id': captain_id,
            'captain_qq': captain_qq,
            'contact1': contact1,
            'contact2': contact2,
            'create_date': create_date,
            'team_points': team_points,
            'members': members
        }

        logger.debug(f"准备保存团队数据: {team_data['team_name']}")

        # 调用服务层保存数据
        if self.team_service:
            try:
                self.team_service.save_team_details(team_data)
                QMessageBox.information(self, "保存成功", "队伍详细信息已保存。")
                logger.info(f"队伍信息保存成功: {team_data['team_name']}")
            except Exception as e:
                QMessageBox.critical(self, "保存失败", f"保存队伍信息时发生错误：{str(e)}")
                logger.error(f"保存队伍信息失败: {team_data['team_name']}, 错误: {e}", exc_info=True)
        else:
            # 如果没有提供 team_service，可以选择保存到本地文件或其他操作
            logger.warning("没有提供 TeamService 实例，无法保存队伍信息")
            QMessageBox.warning(self, "保存失败", "无法保存队伍信息，因为没有提供服务实例。")

    def load_team_data(self, team_data):
        """
        从字典加载团队数据到UI
        :param team_data: dict 包含团队详细信息
        """
        self.team_name_edit.setText(team_data.get('team_name', ''))
        self.team_abbreviation_edit.setText(team_data.get('team_abbreviation', ''))

        logo_path = team_data.get('team_logo')
        if logo_path and os.path.exists(logo_path):
            self.logo_path = logo_path
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap.scaled(
                    self.logo_label.size(), Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ))
                logger.debug(f"加载队伍Logo: {logo_path}")
            else:
                self.logo_label.setText("无法加载Logo")
                logger.warning(f"无法加载Logo图片: {logo_path}")
        else:
            self.logo_label.setText("未设置Logo")
            logger.info("未设置队伍Logo")

        self.captain_id_edit.setText(str(team_data.get('captain_id', '')))
        self.captain_qq_edit.setText(str(team_data.get('captain_qq', '')))
        self.contact1_edit.setText(str(team_data.get('contact1', '')))
        self.contact2_edit.setText(str(team_data.get('contact2', '')))

        create_date = team_data.get('create_date')
        if isinstance(create_date, str):
            # 假设日期格式为 'YYYY-MM-DD'
            try:
                year, month, day = map(int, create_date.split('-'))
                self.create_date_edit.setDate(QDate(year, month, day))
                logger.debug(f"设置成立日期: {create_date}")
            except Exception as e:
                self.create_date_edit.setDate(QDate.currentDate())
                logger.error(f"设置成立日期失败: {create_date}, 错误: {e}")
        elif isinstance(create_date, datetime.date):
            self.create_date_edit.setDate(QDate(create_date.year, create_date.month, create_date.day))
            logger.debug(f"设置成立日期: {create_date}")
        else:
            self.create_date_edit.setDate(QDate.currentDate())
            logger.info("使用当前日期作为成立日期")

        self.team_points_spin.setValue(team_data.get('team_points', 0))
        logger.debug(f"设置队伍积分: {team_data.get('team_points', 0)}")

        # 加载队员信息
        members = team_data.get('members', [])
        self.members_table.setRowCount(0)  # 清空现有行
        for member in members:
            row_position = self.members_table.rowCount()
            self.members_table.insertRow(row_position)
            self.members_table.setItem(row_position, 0, QTableWidgetItem(member.get('nickname', '')))
            self.members_table.setItem(row_position, 1, QTableWidgetItem(member.get('position', '')))
            self.members_table.setItem(row_position, 2, QTableWidgetItem(member.get('game_id', '')))
            self.members_table.setItem(row_position, 3, QTableWidgetItem(str(member.get('individual_points', ''))))
            self.members_table.setItem(row_position, 4, QTableWidgetItem(member.get('qq_number', '')))
            self.members_table.setItem(row_position, 5, QTableWidgetItem(member.get('role', '')))
            logger.debug(f"加载队员信息: {member.get('nickname', '')}")

    def get_team_data(self):
        """
        从UI获取团队数据并返回为字典
        :return: dict 包含团队详细信息
        """
        team_data = {
            'team_name': self.team_name_edit.text().strip(),
            'team_abbreviation': self.team_abbreviation_edit.text().strip(),
            'team_logo': self.logo_path,
            'captain_id': self.captain_id_edit.text().strip(),
            'captain_qq': self.captain_qq_edit.text().strip(),
            'contact1': self.contact1_edit.text().strip(),
            'contact2': self.contact2_edit.text().strip(),
            'create_date': self.create_date_edit.date().toPyDate(),
            'team_points': self.team_points_spin.value(),
            'members': []
        }

        for row in range(self.members_table.rowCount()):
            member = {
                'nickname': self.members_table.item(row, 0).text().strip() if self.members_table.item(row, 0) else '',
                'position': self.members_table.item(row, 1).text().strip() if self.members_table.item(row, 1) else '',
                'game_id': self.members_table.item(row, 2).text().strip() if self.members_table.item(row, 2) else '',
                'individual_points': int(self.members_table.item(row, 3).text().strip()) if self.members_table.item(row,
                                                                                                                    3) and self.members_table.item(
                    row, 3).text().strip().isdigit() else 0,
                'qq_number': self.members_table.item(row, 4).text().strip() if self.members_table.item(row, 4) else '',
                'role': self.members_table.item(row, 5).text().strip() if self.members_table.item(row, 5) else '',
            }
            team_data['members'].append(member)

        logger.debug(f"获取团队数据: {team_data['team_name']}")
        return team_data
