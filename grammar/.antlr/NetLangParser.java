// Generated from /home/ubuntu/NetLang/grammar/NetLang.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class NetLangParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		NETWORK=1, DEVICE=2, SUBNET=3, INTERFACE=4, CONNECT=5, TO=6, IP=7, MASK=8, 
		GATEWAY=9, BANDWIDTH=10, LATENCY=11, ROUTER=12, SWITCH=13, HOST=14, KBPS=15, 
		MBPS=16, GBPS=17, MS=18, US=19, LBRACE=20, RBRACE=21, DOT=22, SLASH=23, 
		ID=24, INT=25, WS=26, COMMENT=27;
	public static final int
		RULE_program = 0, RULE_networkBlock = 1, RULE_networkBody = 2, RULE_statement = 3, 
		RULE_deviceDecl = 4, RULE_deviceBody = 5, RULE_deviceProp = 6, RULE_deviceType = 7, 
		RULE_subnetDecl = 8, RULE_interfaceDecl = 9, RULE_connectDecl = 10, RULE_portRef = 11, 
		RULE_linkProps = 12, RULE_linkProp = 13, RULE_speedUnit = 14, RULE_timeUnit = 15, 
		RULE_ipAddress = 16;
	private static String[] makeRuleNames() {
		return new String[] {
			"program", "networkBlock", "networkBody", "statement", "deviceDecl", 
			"deviceBody", "deviceProp", "deviceType", "subnetDecl", "interfaceDecl", 
			"connectDecl", "portRef", "linkProps", "linkProp", "speedUnit", "timeUnit", 
			"ipAddress"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'network'", "'device'", "'subnet'", "'interface'", "'connect'", 
			"'to'", "'ip'", "'mask'", "'gateway'", "'bandwidth'", "'latency'", "'router'", 
			"'switch'", "'host'", "'Kbps'", "'Mbps'", "'Gbps'", "'ms'", "'us'", "'{'", 
			"'}'", "'.'", "'/'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "NETWORK", "DEVICE", "SUBNET", "INTERFACE", "CONNECT", "TO", "IP", 
			"MASK", "GATEWAY", "BANDWIDTH", "LATENCY", "ROUTER", "SWITCH", "HOST", 
			"KBPS", "MBPS", "GBPS", "MS", "US", "LBRACE", "RBRACE", "DOT", "SLASH", 
			"ID", "INT", "WS", "COMMENT"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "NetLang.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public NetLangParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ProgramContext extends ParserRuleContext {
		public NetworkBlockContext networkBlock() {
			return getRuleContext(NetworkBlockContext.class,0);
		}
		public TerminalNode EOF() { return getToken(NetLangParser.EOF, 0); }
		public ProgramContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_program; }
	}

	public final ProgramContext program() throws RecognitionException {
		ProgramContext _localctx = new ProgramContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_program);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(34);
			networkBlock();
			setState(35);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class NetworkBlockContext extends ParserRuleContext {
		public TerminalNode NETWORK() { return getToken(NetLangParser.NETWORK, 0); }
		public TerminalNode ID() { return getToken(NetLangParser.ID, 0); }
		public TerminalNode LBRACE() { return getToken(NetLangParser.LBRACE, 0); }
		public NetworkBodyContext networkBody() {
			return getRuleContext(NetworkBodyContext.class,0);
		}
		public TerminalNode RBRACE() { return getToken(NetLangParser.RBRACE, 0); }
		public NetworkBlockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_networkBlock; }
	}

	public final NetworkBlockContext networkBlock() throws RecognitionException {
		NetworkBlockContext _localctx = new NetworkBlockContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_networkBlock);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(37);
			match(NETWORK);
			setState(38);
			match(ID);
			setState(39);
			match(LBRACE);
			setState(40);
			networkBody();
			setState(41);
			match(RBRACE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class NetworkBodyContext extends ParserRuleContext {
		public List<StatementContext> statement() {
			return getRuleContexts(StatementContext.class);
		}
		public StatementContext statement(int i) {
			return getRuleContext(StatementContext.class,i);
		}
		public NetworkBodyContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_networkBody; }
	}

	public final NetworkBodyContext networkBody() throws RecognitionException {
		NetworkBodyContext _localctx = new NetworkBodyContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_networkBody);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(46);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 60L) != 0)) {
				{
				{
				setState(43);
				statement();
				}
				}
				setState(48);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class StatementContext extends ParserRuleContext {
		public DeviceDeclContext deviceDecl() {
			return getRuleContext(DeviceDeclContext.class,0);
		}
		public SubnetDeclContext subnetDecl() {
			return getRuleContext(SubnetDeclContext.class,0);
		}
		public InterfaceDeclContext interfaceDecl() {
			return getRuleContext(InterfaceDeclContext.class,0);
		}
		public ConnectDeclContext connectDecl() {
			return getRuleContext(ConnectDeclContext.class,0);
		}
		public StatementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_statement; }
	}

	public final StatementContext statement() throws RecognitionException {
		StatementContext _localctx = new StatementContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_statement);
		try {
			setState(53);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case DEVICE:
				enterOuterAlt(_localctx, 1);
				{
				setState(49);
				deviceDecl();
				}
				break;
			case SUBNET:
				enterOuterAlt(_localctx, 2);
				{
				setState(50);
				subnetDecl();
				}
				break;
			case INTERFACE:
				enterOuterAlt(_localctx, 3);
				{
				setState(51);
				interfaceDecl();
				}
				break;
			case CONNECT:
				enterOuterAlt(_localctx, 4);
				{
				setState(52);
				connectDecl();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class DeviceDeclContext extends ParserRuleContext {
		public TerminalNode DEVICE() { return getToken(NetLangParser.DEVICE, 0); }
		public TerminalNode ID() { return getToken(NetLangParser.ID, 0); }
		public DeviceTypeContext deviceType() {
			return getRuleContext(DeviceTypeContext.class,0);
		}
		public TerminalNode LBRACE() { return getToken(NetLangParser.LBRACE, 0); }
		public DeviceBodyContext deviceBody() {
			return getRuleContext(DeviceBodyContext.class,0);
		}
		public TerminalNode RBRACE() { return getToken(NetLangParser.RBRACE, 0); }
		public DeviceDeclContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_deviceDecl; }
	}

	public final DeviceDeclContext deviceDecl() throws RecognitionException {
		DeviceDeclContext _localctx = new DeviceDeclContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_deviceDecl);
		try {
			setState(65);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,2,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(55);
				match(DEVICE);
				setState(56);
				match(ID);
				setState(57);
				deviceType();
				setState(58);
				match(LBRACE);
				setState(59);
				deviceBody();
				setState(60);
				match(RBRACE);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(62);
				match(DEVICE);
				setState(63);
				match(ID);
				setState(64);
				deviceType();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class DeviceBodyContext extends ParserRuleContext {
		public List<DevicePropContext> deviceProp() {
			return getRuleContexts(DevicePropContext.class);
		}
		public DevicePropContext deviceProp(int i) {
			return getRuleContext(DevicePropContext.class,i);
		}
		public DeviceBodyContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_deviceBody; }
	}

	public final DeviceBodyContext deviceBody() throws RecognitionException {
		DeviceBodyContext _localctx = new DeviceBodyContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_deviceBody);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(70);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==SUBNET || _la==GATEWAY) {
				{
				{
				setState(67);
				deviceProp();
				}
				}
				setState(72);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class DevicePropContext extends ParserRuleContext {
		public TerminalNode SUBNET() { return getToken(NetLangParser.SUBNET, 0); }
		public TerminalNode ID() { return getToken(NetLangParser.ID, 0); }
		public TerminalNode GATEWAY() { return getToken(NetLangParser.GATEWAY, 0); }
		public IpAddressContext ipAddress() {
			return getRuleContext(IpAddressContext.class,0);
		}
		public DevicePropContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_deviceProp; }
	}

	public final DevicePropContext deviceProp() throws RecognitionException {
		DevicePropContext _localctx = new DevicePropContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_deviceProp);
		try {
			setState(77);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case SUBNET:
				enterOuterAlt(_localctx, 1);
				{
				setState(73);
				match(SUBNET);
				setState(74);
				match(ID);
				}
				break;
			case GATEWAY:
				enterOuterAlt(_localctx, 2);
				{
				setState(75);
				match(GATEWAY);
				setState(76);
				ipAddress();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class DeviceTypeContext extends ParserRuleContext {
		public TerminalNode ROUTER() { return getToken(NetLangParser.ROUTER, 0); }
		public TerminalNode SWITCH() { return getToken(NetLangParser.SWITCH, 0); }
		public TerminalNode HOST() { return getToken(NetLangParser.HOST, 0); }
		public DeviceTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_deviceType; }
	}

	public final DeviceTypeContext deviceType() throws RecognitionException {
		DeviceTypeContext _localctx = new DeviceTypeContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_deviceType);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(79);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 28672L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class SubnetDeclContext extends ParserRuleContext {
		public TerminalNode SUBNET() { return getToken(NetLangParser.SUBNET, 0); }
		public TerminalNode ID() { return getToken(NetLangParser.ID, 0); }
		public IpAddressContext ipAddress() {
			return getRuleContext(IpAddressContext.class,0);
		}
		public TerminalNode SLASH() { return getToken(NetLangParser.SLASH, 0); }
		public TerminalNode INT() { return getToken(NetLangParser.INT, 0); }
		public SubnetDeclContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_subnetDecl; }
	}

	public final SubnetDeclContext subnetDecl() throws RecognitionException {
		SubnetDeclContext _localctx = new SubnetDeclContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_subnetDecl);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(81);
			match(SUBNET);
			setState(82);
			match(ID);
			setState(83);
			ipAddress();
			setState(84);
			match(SLASH);
			setState(85);
			match(INT);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class InterfaceDeclContext extends ParserRuleContext {
		public TerminalNode INTERFACE() { return getToken(NetLangParser.INTERFACE, 0); }
		public List<TerminalNode> ID() { return getTokens(NetLangParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(NetLangParser.ID, i);
		}
		public TerminalNode IP() { return getToken(NetLangParser.IP, 0); }
		public List<IpAddressContext> ipAddress() {
			return getRuleContexts(IpAddressContext.class);
		}
		public IpAddressContext ipAddress(int i) {
			return getRuleContext(IpAddressContext.class,i);
		}
		public TerminalNode MASK() { return getToken(NetLangParser.MASK, 0); }
		public InterfaceDeclContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_interfaceDecl; }
	}

	public final InterfaceDeclContext interfaceDecl() throws RecognitionException {
		InterfaceDeclContext _localctx = new InterfaceDeclContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_interfaceDecl);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(87);
			match(INTERFACE);
			setState(88);
			match(ID);
			setState(89);
			match(ID);
			setState(90);
			match(IP);
			setState(91);
			ipAddress();
			setState(92);
			match(MASK);
			setState(93);
			ipAddress();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ConnectDeclContext extends ParserRuleContext {
		public TerminalNode CONNECT() { return getToken(NetLangParser.CONNECT, 0); }
		public List<PortRefContext> portRef() {
			return getRuleContexts(PortRefContext.class);
		}
		public PortRefContext portRef(int i) {
			return getRuleContext(PortRefContext.class,i);
		}
		public TerminalNode TO() { return getToken(NetLangParser.TO, 0); }
		public LinkPropsContext linkProps() {
			return getRuleContext(LinkPropsContext.class,0);
		}
		public ConnectDeclContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_connectDecl; }
	}

	public final ConnectDeclContext connectDecl() throws RecognitionException {
		ConnectDeclContext _localctx = new ConnectDeclContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_connectDecl);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(95);
			match(CONNECT);
			setState(96);
			portRef();
			setState(97);
			match(TO);
			setState(98);
			portRef();
			setState(100);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==BANDWIDTH || _la==LATENCY) {
				{
				setState(99);
				linkProps();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PortRefContext extends ParserRuleContext {
		public List<TerminalNode> ID() { return getTokens(NetLangParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(NetLangParser.ID, i);
		}
		public TerminalNode DOT() { return getToken(NetLangParser.DOT, 0); }
		public PortRefContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_portRef; }
	}

	public final PortRefContext portRef() throws RecognitionException {
		PortRefContext _localctx = new PortRefContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_portRef);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(102);
			match(ID);
			setState(103);
			match(DOT);
			setState(104);
			match(ID);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class LinkPropsContext extends ParserRuleContext {
		public List<LinkPropContext> linkProp() {
			return getRuleContexts(LinkPropContext.class);
		}
		public LinkPropContext linkProp(int i) {
			return getRuleContext(LinkPropContext.class,i);
		}
		public LinkPropsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_linkProps; }
	}

	public final LinkPropsContext linkProps() throws RecognitionException {
		LinkPropsContext _localctx = new LinkPropsContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_linkProps);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(107); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(106);
				linkProp();
				}
				}
				setState(109); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==BANDWIDTH || _la==LATENCY );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class LinkPropContext extends ParserRuleContext {
		public TerminalNode BANDWIDTH() { return getToken(NetLangParser.BANDWIDTH, 0); }
		public TerminalNode INT() { return getToken(NetLangParser.INT, 0); }
		public SpeedUnitContext speedUnit() {
			return getRuleContext(SpeedUnitContext.class,0);
		}
		public TerminalNode LATENCY() { return getToken(NetLangParser.LATENCY, 0); }
		public TimeUnitContext timeUnit() {
			return getRuleContext(TimeUnitContext.class,0);
		}
		public LinkPropContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_linkProp; }
	}

	public final LinkPropContext linkProp() throws RecognitionException {
		LinkPropContext _localctx = new LinkPropContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_linkProp);
		try {
			setState(117);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case BANDWIDTH:
				enterOuterAlt(_localctx, 1);
				{
				setState(111);
				match(BANDWIDTH);
				setState(112);
				match(INT);
				setState(113);
				speedUnit();
				}
				break;
			case LATENCY:
				enterOuterAlt(_localctx, 2);
				{
				setState(114);
				match(LATENCY);
				setState(115);
				match(INT);
				setState(116);
				timeUnit();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class SpeedUnitContext extends ParserRuleContext {
		public TerminalNode KBPS() { return getToken(NetLangParser.KBPS, 0); }
		public TerminalNode MBPS() { return getToken(NetLangParser.MBPS, 0); }
		public TerminalNode GBPS() { return getToken(NetLangParser.GBPS, 0); }
		public SpeedUnitContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_speedUnit; }
	}

	public final SpeedUnitContext speedUnit() throws RecognitionException {
		SpeedUnitContext _localctx = new SpeedUnitContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_speedUnit);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(119);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 229376L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class TimeUnitContext extends ParserRuleContext {
		public TerminalNode MS() { return getToken(NetLangParser.MS, 0); }
		public TerminalNode US() { return getToken(NetLangParser.US, 0); }
		public TimeUnitContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_timeUnit; }
	}

	public final TimeUnitContext timeUnit() throws RecognitionException {
		TimeUnitContext _localctx = new TimeUnitContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_timeUnit);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(121);
			_la = _input.LA(1);
			if ( !(_la==MS || _la==US) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class IpAddressContext extends ParserRuleContext {
		public List<TerminalNode> INT() { return getTokens(NetLangParser.INT); }
		public TerminalNode INT(int i) {
			return getToken(NetLangParser.INT, i);
		}
		public List<TerminalNode> DOT() { return getTokens(NetLangParser.DOT); }
		public TerminalNode DOT(int i) {
			return getToken(NetLangParser.DOT, i);
		}
		public IpAddressContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ipAddress; }
	}

	public final IpAddressContext ipAddress() throws RecognitionException {
		IpAddressContext _localctx = new IpAddressContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_ipAddress);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(123);
			match(INT);
			setState(124);
			match(DOT);
			setState(125);
			match(INT);
			setState(126);
			match(DOT);
			setState(127);
			match(INT);
			setState(128);
			match(DOT);
			setState(129);
			match(INT);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\u0004\u0001\u001b\u0084\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001"+
		"\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004"+
		"\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007"+
		"\u0002\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b"+
		"\u0002\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002\u000f\u0007"+
		"\u000f\u0002\u0010\u0007\u0010\u0001\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0002\u0005\u0002-\b\u0002\n\u0002\f\u00020\t\u0002\u0001\u0003\u0001"+
		"\u0003\u0001\u0003\u0001\u0003\u0003\u00036\b\u0003\u0001\u0004\u0001"+
		"\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001"+
		"\u0004\u0001\u0004\u0001\u0004\u0003\u0004B\b\u0004\u0001\u0005\u0005"+
		"\u0005E\b\u0005\n\u0005\f\u0005H\t\u0005\u0001\u0006\u0001\u0006\u0001"+
		"\u0006\u0001\u0006\u0003\u0006N\b\u0006\u0001\u0007\u0001\u0007\u0001"+
		"\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001\t\u0001\t\u0001\t\u0001"+
		"\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\n\u0001\n\u0001\n\u0001\n\u0001"+
		"\n\u0003\ne\b\n\u0001\u000b\u0001\u000b\u0001\u000b\u0001\u000b\u0001"+
		"\f\u0004\fl\b\f\u000b\f\f\fm\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001"+
		"\r\u0003\rv\b\r\u0001\u000e\u0001\u000e\u0001\u000f\u0001\u000f\u0001"+
		"\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001"+
		"\u0010\u0001\u0010\u0001\u0010\u0000\u0000\u0011\u0000\u0002\u0004\u0006"+
		"\b\n\f\u000e\u0010\u0012\u0014\u0016\u0018\u001a\u001c\u001e \u0000\u0003"+
		"\u0001\u0000\f\u000e\u0001\u0000\u000f\u0011\u0001\u0000\u0012\u0013|"+
		"\u0000\"\u0001\u0000\u0000\u0000\u0002%\u0001\u0000\u0000\u0000\u0004"+
		".\u0001\u0000\u0000\u0000\u00065\u0001\u0000\u0000\u0000\bA\u0001\u0000"+
		"\u0000\u0000\nF\u0001\u0000\u0000\u0000\fM\u0001\u0000\u0000\u0000\u000e"+
		"O\u0001\u0000\u0000\u0000\u0010Q\u0001\u0000\u0000\u0000\u0012W\u0001"+
		"\u0000\u0000\u0000\u0014_\u0001\u0000\u0000\u0000\u0016f\u0001\u0000\u0000"+
		"\u0000\u0018k\u0001\u0000\u0000\u0000\u001au\u0001\u0000\u0000\u0000\u001c"+
		"w\u0001\u0000\u0000\u0000\u001ey\u0001\u0000\u0000\u0000 {\u0001\u0000"+
		"\u0000\u0000\"#\u0003\u0002\u0001\u0000#$\u0005\u0000\u0000\u0001$\u0001"+
		"\u0001\u0000\u0000\u0000%&\u0005\u0001\u0000\u0000&\'\u0005\u0018\u0000"+
		"\u0000\'(\u0005\u0014\u0000\u0000()\u0003\u0004\u0002\u0000)*\u0005\u0015"+
		"\u0000\u0000*\u0003\u0001\u0000\u0000\u0000+-\u0003\u0006\u0003\u0000"+
		",+\u0001\u0000\u0000\u0000-0\u0001\u0000\u0000\u0000.,\u0001\u0000\u0000"+
		"\u0000./\u0001\u0000\u0000\u0000/\u0005\u0001\u0000\u0000\u00000.\u0001"+
		"\u0000\u0000\u000016\u0003\b\u0004\u000026\u0003\u0010\b\u000036\u0003"+
		"\u0012\t\u000046\u0003\u0014\n\u000051\u0001\u0000\u0000\u000052\u0001"+
		"\u0000\u0000\u000053\u0001\u0000\u0000\u000054\u0001\u0000\u0000\u0000"+
		"6\u0007\u0001\u0000\u0000\u000078\u0005\u0002\u0000\u000089\u0005\u0018"+
		"\u0000\u00009:\u0003\u000e\u0007\u0000:;\u0005\u0014\u0000\u0000;<\u0003"+
		"\n\u0005\u0000<=\u0005\u0015\u0000\u0000=B\u0001\u0000\u0000\u0000>?\u0005"+
		"\u0002\u0000\u0000?@\u0005\u0018\u0000\u0000@B\u0003\u000e\u0007\u0000"+
		"A7\u0001\u0000\u0000\u0000A>\u0001\u0000\u0000\u0000B\t\u0001\u0000\u0000"+
		"\u0000CE\u0003\f\u0006\u0000DC\u0001\u0000\u0000\u0000EH\u0001\u0000\u0000"+
		"\u0000FD\u0001\u0000\u0000\u0000FG\u0001\u0000\u0000\u0000G\u000b\u0001"+
		"\u0000\u0000\u0000HF\u0001\u0000\u0000\u0000IJ\u0005\u0003\u0000\u0000"+
		"JN\u0005\u0018\u0000\u0000KL\u0005\t\u0000\u0000LN\u0003 \u0010\u0000"+
		"MI\u0001\u0000\u0000\u0000MK\u0001\u0000\u0000\u0000N\r\u0001\u0000\u0000"+
		"\u0000OP\u0007\u0000\u0000\u0000P\u000f\u0001\u0000\u0000\u0000QR\u0005"+
		"\u0003\u0000\u0000RS\u0005\u0018\u0000\u0000ST\u0003 \u0010\u0000TU\u0005"+
		"\u0017\u0000\u0000UV\u0005\u0019\u0000\u0000V\u0011\u0001\u0000\u0000"+
		"\u0000WX\u0005\u0004\u0000\u0000XY\u0005\u0018\u0000\u0000YZ\u0005\u0018"+
		"\u0000\u0000Z[\u0005\u0007\u0000\u0000[\\\u0003 \u0010\u0000\\]\u0005"+
		"\b\u0000\u0000]^\u0003 \u0010\u0000^\u0013\u0001\u0000\u0000\u0000_`\u0005"+
		"\u0005\u0000\u0000`a\u0003\u0016\u000b\u0000ab\u0005\u0006\u0000\u0000"+
		"bd\u0003\u0016\u000b\u0000ce\u0003\u0018\f\u0000dc\u0001\u0000\u0000\u0000"+
		"de\u0001\u0000\u0000\u0000e\u0015\u0001\u0000\u0000\u0000fg\u0005\u0018"+
		"\u0000\u0000gh\u0005\u0016\u0000\u0000hi\u0005\u0018\u0000\u0000i\u0017"+
		"\u0001\u0000\u0000\u0000jl\u0003\u001a\r\u0000kj\u0001\u0000\u0000\u0000"+
		"lm\u0001\u0000\u0000\u0000mk\u0001\u0000\u0000\u0000mn\u0001\u0000\u0000"+
		"\u0000n\u0019\u0001\u0000\u0000\u0000op\u0005\n\u0000\u0000pq\u0005\u0019"+
		"\u0000\u0000qv\u0003\u001c\u000e\u0000rs\u0005\u000b\u0000\u0000st\u0005"+
		"\u0019\u0000\u0000tv\u0003\u001e\u000f\u0000uo\u0001\u0000\u0000\u0000"+
		"ur\u0001\u0000\u0000\u0000v\u001b\u0001\u0000\u0000\u0000wx\u0007\u0001"+
		"\u0000\u0000x\u001d\u0001\u0000\u0000\u0000yz\u0007\u0002\u0000\u0000"+
		"z\u001f\u0001\u0000\u0000\u0000{|\u0005\u0019\u0000\u0000|}\u0005\u0016"+
		"\u0000\u0000}~\u0005\u0019\u0000\u0000~\u007f\u0005\u0016\u0000\u0000"+
		"\u007f\u0080\u0005\u0019\u0000\u0000\u0080\u0081\u0005\u0016\u0000\u0000"+
		"\u0081\u0082\u0005\u0019\u0000\u0000\u0082!\u0001\u0000\u0000\u0000\b"+
		".5AFMdmu";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}